"""Flashcard Quiz Tool — implements the universal BaseTool interface.

This is the tool's core: schema declaration + programmatic execution.
Decoupled from CLI parsing and display — those are handled by
BaseTool.main() and the display module respectively.
"""

from __future__ import annotations

from typing import Any

from ayra_lib.config import VaultConfig
from ayra_lib.parsers import VaultFlashcardParser
from ayra_lib.tool_interface import BaseTool, InputField, ToolOutput, ToolSchema, ToolStatus
from ayra_lib.types import Flashcard

from flashcard_quiz.display import (
    print_answer,
    print_card_list,
    print_correct,
    print_header,
    print_incorrect,
    print_question,
    print_quit,
    print_results,
)
from flashcard_quiz.quiz import SelectionStrategy, compute_result, select_cards


class FlashcardQuizTool(BaseTool):
    """Interactive flashcard quiz from vault flashcards.md files.

    Modes:
      - Programmatic: `--input '{"topic": "agent-memory"}'` → JSON ToolOutput
      - Interactive: `--topic agent-memory` → pretty terminal quiz
      - List: `--topic agent-memory --list` → numbered card list
      - Schema: `--schema` → full JSON schema for agent introspection
    """

    def __init__(self, config: VaultConfig | None = None) -> None:
        """Initialize with optional vault config (Dependency Injection)."""
        self._config = config or VaultConfig()

    def schema(self) -> ToolSchema:
        """Declare what this tool expects and returns."""
        return ToolSchema(
            name="flashcard-quiz",
            version="1.1.0",
            description=(
                "Interactive CLI quiz from vault flashcards. "
                "Parses <details>/<summary> markdown format, supports multiple "
                "selection strategies, tracks score with missed questions."
            ),
            inputs=(
                InputField(
                    name="topic",
                    type="string",
                    required=True,
                    description=(
                        "Topic name or path relative to tech/ "
                        "(e.g., 'agent-memory', 'python/asyncio')"
                    ),
                ),
                InputField(
                    name="count",
                    type="integer",
                    required=False,
                    default=10,
                    description="Number of questions (0 = all)",
                ),
                InputField(
                    name="mode",
                    type="string",
                    required=False,
                    default="random",
                    enum=("random", "sequential", "reverse"),
                    description="Question selection strategy",
                ),
                InputField(
                    name="show-hint",
                    type="boolean",
                    required=False,
                    default=False,
                    description="Show section name as hint before answering",
                ),
                InputField(
                    name="list",
                    type="boolean",
                    required=False,
                    default=False,
                    description="List all available cards and exit (no quiz)",
                ),
            ),
            output_description=(
                "ToolOutput with data containing: cards_found (int), "
                "quiz_result {correct, total, percentage, grade, missed[]}, "
                "cards[] (in list mode)"
            ),
            tags=("revision", "flashcards", "quiz", "learning"),
            examples=(
                {"topic": "agent-memory", "count": 5, "mode": "random"},
                {"topic": "python/asyncio", "list": True},
                {"topic": "agent-memory", "count": 0, "mode": "sequential"},
            ),
        )

    def _load_cards(self, topic: str) -> tuple[list[Flashcard], str | None]:
        """Resolve topic → parse flashcards. Returns (cards, error_msg)."""
        fc_path = self._config.find_flashcards(topic)
        if fc_path is None:
            return [], f"No flashcards.md found for topic: {topic}"

        try:
            parser = VaultFlashcardParser(fc_path)
            cards = parser.load()
        except FileNotFoundError as e:
            return [], str(e)

        if not cards:
            return [], f"No flashcard blocks found in: {fc_path}"

        return cards, None

    def execute(self, inputs: dict[str, Any]) -> ToolOutput:
        """Programmatic execution — JSON in, ToolOutput out.

        This path is used by agents. No terminal I/O, no ANSI,
        no interactive prompts. Pure data transformation.
        """
        topic: str = inputs["topic"]
        count: int = inputs.get("count", 10)
        mode_str: str = inputs.get("mode", "random")
        list_mode: bool = inputs.get("list", False)

        # Load cards
        cards, error = self._load_cards(topic)
        if error:
            return self._make_error(error)

        # List mode: return all cards as structured data
        if list_mode:
            return ToolOutput(
                status=ToolStatus.SUCCESS,
                tool="flashcard-quiz",
                version="1.1.0",
                message=f"Found {len(cards)} flashcards for topic '{topic}'",
                data={
                    "cards_found": len(cards),
                    "cards": [
                        {
                            "index": c.card_index,
                            "question": c.question,
                            "answer": c.answer,
                            "section": c.section,
                        }
                        for c in cards
                    ],
                },
            )

        # Quiz mode (non-interactive): select cards, return them for agent to use
        strategy = SelectionStrategy(mode_str)
        selected = select_cards(cards, count, strategy)

        return ToolOutput(
            status=ToolStatus.SUCCESS,
            tool="flashcard-quiz",
            version="1.1.0",
            message=f"Selected {len(selected)} of {len(cards)} flashcards for topic '{topic}'",
            data={
                "cards_found": len(cards),
                "cards_selected": len(selected),
                "topic": topic,
                "mode": mode_str,
                "cards": [
                    {
                        "index": c.card_index,
                        "question": c.question,
                        "answer": c.answer,
                        "section": c.section,
                    }
                    for c in selected
                ],
            },
        )

    def run_interactive(self, inputs: dict[str, Any]) -> None:
        """Human-friendly interactive quiz with terminal UI."""
        import sys

        topic: str = inputs["topic"]
        count: int = inputs.get("count", 10)
        mode_str: str = inputs.get("mode", "random")
        show_hint: bool = inputs.get("show_hint", False) or inputs.get("show-hint", False)
        list_mode: bool = inputs.get("list", False)

        # Load cards
        cards, error = self._load_cards(topic)
        if error:
            print(f"❌ {error}", file=sys.stderr)
            sys.exit(1)

        rel_path = "tech/" + topic + "/flashcards.md"
        print(f"  📂 Found {len(cards)} flashcards in: {rel_path}")

        # List mode
        if list_mode:
            print_card_list(cards)
            return

        # Interactive quiz
        strategy = SelectionStrategy(mode_str)
        selected = select_cards(cards, count, strategy)
        total = len(selected)

        print_header(total)

        correct = 0
        missed: list[str] = []
        answered = 0

        for i, card in enumerate(selected, 1):
            print_question(i, total, card, show_hint=show_hint)

            try:
                input("  [Press ENTER to reveal answer] ")
            except (EOFError, KeyboardInterrupt):
                print_quit()
                break

            print_answer(card)

            # Self-rating
            rating = self._prompt_rating()
            if rating is None:
                print_quit()
                answered = i
                break

            answered = i
            if rating == "y":
                correct += 1
                print_correct()
            else:
                missed.append(card.question)
                print_incorrect()

        result = compute_result(correct, answered, missed)
        print_results(result)

    @staticmethod
    def _prompt_rating() -> str | None:
        """Prompt user for self-rating. Returns 'y', 'n', or None for quit."""
        while True:
            try:
                response = input("  Did you get it? [y/n/q]: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                return None

            if response in ("y", "yes"):
                return "y"
            if response in ("n", "no"):
                return "n"
            if response in ("q", "quit"):
                return None
