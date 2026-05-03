"""CLI entrypoint — composition root for youtube-transcript tool."""

from youtube_transcript.tool import YouTubeTranscriptTool


def main() -> None:
    """Entrypoint wired to console_scripts."""
    tool = YouTubeTranscriptTool()
    tool.main()


if __name__ == "__main__":
    main()
