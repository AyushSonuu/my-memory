"""CLI entrypoint — instantiates the tool and delegates to BaseTool.main().

This is the thinnest possible composition root:
  1. Create the tool instance
  2. Call main() — BaseTool handles --schema, --input, and interactive dispatch
"""

from flashcard_quiz.tool import FlashcardQuizTool


def main() -> None:
    """Console script entrypoint."""
    FlashcardQuizTool().main()


if __name__ == "__main__":
    main()
