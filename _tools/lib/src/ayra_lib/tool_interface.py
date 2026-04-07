"""Universal Tool Interface — the contract every Ayra tool must implement.

This is the core abstraction that makes tools agent-agnostic. Any agent
(Ayra, Claude Code, Codex, custom scripts) can:
  1. DISCOVER tools via registry.json
  2. INTROSPECT a tool via `tool --schema` (get full JSON schema)
  3. EXECUTE a tool via `tool --input '{"key": "value"}'` (JSON in → JSON out)
  4. PARSE results from a standard ToolOutput envelope

Two execution modes:
  - INTERACTIVE: pretty terminal output for humans (default)
  - PROGRAMMATIC: `--input '{...}'` → pure JSON to stdout (for agents)

Protocol-based design (DI): tools implement BaseTool, callers depend on the protocol.
"""

from __future__ import annotations

import json
import sys
import traceback
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import StrEnum, auto
from typing import Any

from ayra_lib.config import IST

# ──────────────────────────────────────────────
# Standard Output Envelope
# ──────────────────────────────────────────────


class ToolStatus(StrEnum):
    """Outcome status of a tool execution."""

    SUCCESS = auto()
    ERROR = auto()
    PARTIAL = auto()  # e.g., quiz ended early


@dataclass(frozen=True, slots=True)
class ToolOutput:
    """Standard envelope for every tool's output.

    Every tool, regardless of what it does, returns this structure.
    Agents parse this — not raw text, not ad-hoc dicts.

    Serializable to JSON via .to_json() / .to_dict().
    """

    status: ToolStatus
    tool: str  # tool name
    version: str  # tool version
    data: dict[str, Any] = field(default_factory=dict)  # tool-specific payload
    message: str = ""  # human-readable summary
    errors: tuple[str, ...] = ()  # error messages if status != SUCCESS
    timestamp: str = field(default_factory=lambda: datetime.now(IST).isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Convert to a plain dict (JSON-serializable)."""
        d = asdict(self)
        d["status"] = self.status.value
        d["errors"] = list(self.errors)
        return d

    def to_json(self, *, indent: int = 2) -> str:
        """Serialize to formatted JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# ──────────────────────────────────────────────
# Input Schema Declaration
# ──────────────────────────────────────────────


@dataclass(frozen=True, slots=True)
class InputField:
    """Schema declaration for a single tool input parameter.

    Used by `--schema` to tell agents exactly what a tool expects.
    """

    name: str
    type: str  # "string" | "integer" | "float" | "boolean" | "path"
    required: bool = True
    description: str = ""
    default: Any = None
    enum: tuple[str, ...] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        d: dict[str, Any] = {
            "name": self.name,
            "type": self.type,
            "required": self.required,
            "description": self.description,
        }
        if self.default is not None:
            d["default"] = self.default
        if self.enum is not None:
            d["enum"] = list(self.enum)
        return d


@dataclass(frozen=True, slots=True)
class ToolSchema:
    """Complete self-describing schema for a tool.

    Returned by `--schema` — tells any agent everything it needs
    to construct a valid `--input` JSON payload.
    """

    name: str
    version: str
    description: str
    inputs: tuple[InputField, ...] = ()
    output_description: str = ""
    tags: tuple[str, ...] = ()
    examples: tuple[dict[str, Any], ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "inputs": [f.to_dict() for f in self.inputs],
            "output_description": self.output_description,
            "tags": list(self.tags),
            "examples": list(self.examples),
        }

    def to_json(self, *, indent: int = 2) -> str:
        """Serialize to formatted JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


# ──────────────────────────────────────────────
# Base Tool Abstract Class
# ──────────────────────────────────────────────


class BaseTool(ABC):
    """Abstract base class that every Ayra tool must extend.

    Provides the universal interface:
      - schema() → ToolSchema (introspection)
      - execute(inputs) → ToolOutput (programmatic execution)
      - run_interactive(inputs) → None (human-friendly terminal mode)
      - main() → handles CLI dispatch (--schema, --input, or interactive)

    Subclasses implement:
      - schema() → declare inputs/outputs
      - execute(inputs) → do the work, return ToolOutput
      - run_interactive(inputs) → pretty terminal version (optional override)

    The main() method handles all dispatch automatically:
      tool --schema              → prints ToolSchema as JSON
      tool --input '{"k":"v"}'   → calls execute(), prints ToolOutput as JSON
      tool --topic foo           → calls run_interactive() with parsed args
    """

    @abstractmethod
    def schema(self) -> ToolSchema:
        """Declare the tool's input/output schema.

        Returned by `tool --schema` for agent introspection.
        Must be pure (no side effects, no I/O).
        """
        ...

    @abstractmethod
    def execute(self, inputs: dict[str, Any]) -> ToolOutput:
        """Execute the tool programmatically.

        Args:
            inputs: Validated input dict matching the schema.

        Returns:
            Standard ToolOutput envelope with results.

        This is the agent-facing execution path.
        Must NOT print to stdout (return data via ToolOutput instead).
        Must NOT call sys.exit() (return error status instead).
        """
        ...

    def run_interactive(self, inputs: dict[str, Any]) -> None:
        """Run the tool in human-friendly interactive mode.

        Override this for tools that have a rich terminal experience
        (e.g., quiz with prompts, progress bars, colored output).

        Default implementation: calls execute() and pretty-prints the result.

        Args:
            inputs: Input dict from CLI argument parsing.
        """
        result = self.execute(inputs)
        if result.status == ToolStatus.ERROR:
            print(f"❌ {result.message}", file=sys.stderr)
            for err in result.errors:
                print(f"   {err}", file=sys.stderr)
            sys.exit(1)

        if result.message:
            print(f"✅ {result.message}")
        if result.data:
            print(json.dumps(result.data, indent=2, ensure_ascii=False))

    def validate_inputs(self, inputs: dict[str, Any]) -> list[str]:
        """Validate inputs against the schema.

        Returns:
            List of validation error messages (empty = valid).
        """
        errors: list[str] = []
        tool_schema = self.schema()

        for field_def in tool_schema.inputs:
            if field_def.required and field_def.name not in inputs and field_def.default is None:
                    errors.append(f"Missing required input: '{field_def.name}'")
            if field_def.name in inputs and field_def.enum is not None:
                val = inputs[field_def.name]
                if val not in field_def.enum:
                    errors.append(
                        f"Invalid value for '{field_def.name}': '{val}'. "
                        f"Must be one of: {list(field_def.enum)}"
                    )

        return errors

    def _apply_defaults(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """Fill in default values for missing optional inputs."""
        result = dict(inputs)
        for field_def in self.schema().inputs:
            if field_def.name not in result and field_def.default is not None:
                result[field_def.name] = field_def.default
        return result

    def _make_error(self, message: str, errors: list[str] | None = None) -> ToolOutput:
        """Convenience: create an error ToolOutput."""
        s = self.schema()
        return ToolOutput(
            status=ToolStatus.ERROR,
            tool=s.name,
            version=s.version,
            message=message,
            errors=tuple(errors or [message]),
        )

    def main(self, args: list[str] | None = None) -> None:
        """Universal CLI dispatcher.

        Handles three modes:
          --schema        → print schema JSON, exit
          --input '{}'    → programmatic mode (JSON in → JSON out)
          (anything else) → interactive mode (parse CLI args)

        This is what gets wired to the console_scripts entrypoint.
        """
        raw_args = args if args is not None else sys.argv[1:]

        # Mode 1: Schema introspection
        if "--schema" in raw_args:
            print(self.schema().to_json())
            return

        # Mode 2: Programmatic execution (agent mode)
        if "--input" in raw_args:
            try:
                idx = raw_args.index("--input")
                json_str = raw_args[idx + 1]
            except (IndexError, ValueError):
                err = self._make_error("--input requires a JSON string argument")
                print(err.to_json(), file=sys.stdout)
                sys.exit(1)

            try:
                inputs = json.loads(json_str)
            except json.JSONDecodeError as e:
                err = self._make_error(f"Invalid JSON input: {e}")
                print(err.to_json(), file=sys.stdout)
                sys.exit(1)

            inputs = self._apply_defaults(inputs)
            validation_errors = self.validate_inputs(inputs)
            if validation_errors:
                err = self._make_error("Input validation failed", validation_errors)
                print(err.to_json(), file=sys.stdout)
                sys.exit(1)

            try:
                result = self.execute(inputs)
            except Exception:
                err = self._make_error(
                    "Tool execution failed",
                    [traceback.format_exc()],
                )
                print(err.to_json(), file=sys.stdout)
                sys.exit(1)

            print(result.to_json())
            return

        # Mode 3: Interactive (parse args, call run_interactive)
        self.run_interactive(self._parse_interactive_args(raw_args))

    def _parse_interactive_args(self, raw_args: list[str]) -> dict[str, Any]:
        """Parse CLI arguments into an input dict for interactive mode.

        Default implementation builds an argparse parser from the schema.
        Override if you need custom CLI argument handling.
        """
        import argparse

        tool_schema = self.schema()
        parser = argparse.ArgumentParser(
            prog=tool_schema.name,
            description=tool_schema.description,
        )

        for field_def in tool_schema.inputs:
            arg_name = f"--{field_def.name}"
            kwargs: dict[str, Any] = {
                "help": field_def.description,
                "required": field_def.required and field_def.default is None,
            }

            if field_def.type == "boolean":
                kwargs["action"] = "store_true"
                kwargs.pop("required", None)
            elif field_def.type == "integer":
                kwargs["type"] = int
            elif field_def.type == "float":
                kwargs["type"] = float

            if field_def.default is not None and field_def.type != "boolean":
                kwargs["default"] = field_def.default

            if field_def.enum is not None and field_def.type != "boolean":
                kwargs["choices"] = list(field_def.enum)

            parser.add_argument(arg_name, **kwargs)

        parsed = parser.parse_args(raw_args)
        return {k: v for k, v in vars(parsed).items() if v is not None}
