"""Tests for the universal tool interface — schema, execute, validate."""

from __future__ import annotations

from pathlib import Path

import pytest
from ayra_lib.config import VaultConfig
from ayra_lib.tool_interface import ToolStatus
from flashcard_quiz.tool import FlashcardQuizTool


@pytest.fixture
def tool(sample_flashcards_file: Path) -> FlashcardQuizTool:
    """Create a tool instance pointed at a temp vault with sample flashcards."""
    # Build a mini vault structure: tmp/tech/test-topic/flashcards.md
    vault_root = sample_flashcards_file.parent.parent
    topic_dir = vault_root / "tech" / "test-topic"
    topic_dir.mkdir(parents=True, exist_ok=True)
    sample_flashcards_file.rename(topic_dir / "flashcards.md")

    # Also need AGENTS.md for repo root detection
    (vault_root / "AGENTS.md").touch()

    config = VaultConfig(repo_root=vault_root)
    return FlashcardQuizTool(config=config)


class TestToolSchema:
    """Test schema introspection (--schema mode)."""

    def test_schema_returns_tool_schema(self) -> None:
        tool = FlashcardQuizTool()
        schema = tool.schema()
        assert schema.name == "flashcard-quiz"
        assert schema.version == "1.1.0"

    def test_schema_has_required_topic(self) -> None:
        schema = FlashcardQuizTool().schema()
        topic_field = next(f for f in schema.inputs if f.name == "topic")
        assert topic_field.required is True
        assert topic_field.type == "string"

    def test_schema_has_optional_count(self) -> None:
        schema = FlashcardQuizTool().schema()
        count_field = next(f for f in schema.inputs if f.name == "count")
        assert count_field.required is False
        assert count_field.default == 10

    def test_schema_has_mode_enum(self) -> None:
        schema = FlashcardQuizTool().schema()
        mode_field = next(f for f in schema.inputs if f.name == "mode")
        assert mode_field.enum is not None
        assert "random" in mode_field.enum
        assert "sequential" in mode_field.enum
        assert "reverse" in mode_field.enum

    def test_schema_serializes_to_json(self) -> None:
        schema = FlashcardQuizTool().schema()
        json_str = schema.to_json()
        assert '"name": "flashcard-quiz"' in json_str
        assert '"inputs"' in json_str

    def test_schema_has_examples(self) -> None:
        schema = FlashcardQuizTool().schema()
        assert len(schema.examples) > 0


class TestToolExecute:
    """Test programmatic execution (--input mode)."""

    def test_execute_list_mode(self, tool: FlashcardQuizTool) -> None:
        result = tool.execute({"topic": "test-topic", "list": True})
        assert result.status == ToolStatus.SUCCESS
        assert result.data["cards_found"] == 4
        assert len(result.data["cards"]) == 4

    def test_execute_list_card_structure(self, tool: FlashcardQuizTool) -> None:
        result = tool.execute({"topic": "test-topic", "list": True})
        card = result.data["cards"][0]
        assert "question" in card
        assert "answer" in card
        assert "section" in card
        assert "index" in card

    def test_execute_quiz_mode(self, tool: FlashcardQuizTool) -> None:
        result = tool.execute({"topic": "test-topic", "count": 2, "mode": "sequential"})
        assert result.status == ToolStatus.SUCCESS
        assert result.data["cards_selected"] == 2
        assert result.data["cards_found"] == 4
        assert len(result.data["cards"]) == 2

    def test_execute_count_zero_returns_all(self, tool: FlashcardQuizTool) -> None:
        result = tool.execute({"topic": "test-topic", "count": 0, "mode": "sequential"})
        assert result.data["cards_selected"] == 4

    def test_execute_nonexistent_topic(self, tool: FlashcardQuizTool) -> None:
        result = tool.execute({"topic": "nonexistent-xyz"})
        assert result.status == ToolStatus.ERROR
        assert "No flashcards" in result.message

    def test_execute_output_envelope(self, tool: FlashcardQuizTool) -> None:
        result = tool.execute({"topic": "test-topic", "list": True})
        assert result.tool == "flashcard-quiz"
        assert result.version == "1.1.0"
        assert result.timestamp  # non-empty

    def test_execute_serializes_to_json(self, tool: FlashcardQuizTool) -> None:
        result = tool.execute({"topic": "test-topic", "list": True})
        json_str = result.to_json()
        assert '"status": "success"' in json_str
        assert '"tool": "flashcard-quiz"' in json_str


class TestToolValidation:
    """Test input validation."""

    def test_missing_required_topic(self) -> None:
        tool = FlashcardQuizTool()
        errors = tool.validate_inputs({"count": 5})
        assert any("topic" in e for e in errors)

    def test_invalid_mode_enum(self) -> None:
        tool = FlashcardQuizTool()
        errors = tool.validate_inputs({"topic": "x", "mode": "invalid"})
        assert any("mode" in e for e in errors)

    def test_valid_inputs_no_errors(self) -> None:
        tool = FlashcardQuizTool()
        errors = tool.validate_inputs({"topic": "agent-memory", "count": 5, "mode": "random"})
        assert errors == []

    def test_defaults_applied(self) -> None:
        tool = FlashcardQuizTool()
        filled = tool._apply_defaults({"topic": "test"})
        assert filled["count"] == 10
        assert filled["mode"] == "random"


class TestToolOutput:
    """Test the ToolOutput envelope."""

    def test_success_output_structure(self, tool: FlashcardQuizTool) -> None:
        result = tool.execute({"topic": "test-topic", "list": True})
        d = result.to_dict()
        assert d["status"] == "success"
        assert isinstance(d["data"], dict)
        assert isinstance(d["errors"], list)
        assert d["tool"] == "flashcard-quiz"

    def test_error_output_structure(self, tool: FlashcardQuizTool) -> None:
        result = tool.execute({"topic": "nonexistent"})
        d = result.to_dict()
        assert d["status"] == "error"
        assert len(d["errors"]) > 0
