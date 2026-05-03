"""Output formatters for transcript data."""

from __future__ import annotations

from youtube_transcript.extractor import TranscriptData


class TranscriptFormatter:
    """Format transcript data in various output formats."""

    @staticmethod
    def format_text(data: TranscriptData) -> str:
        """Format as plain text with basic metadata header."""
        lines = []

        if data.metadata.title:
            lines.append(f"Title: {data.metadata.title}")
        if data.metadata.channel:
            lines.append(f"Channel: {data.metadata.channel}")
        if data.metadata.duration_seconds:
            minutes, seconds = divmod(data.metadata.duration_seconds, 60)
            lines.append(f"Duration: {minutes}:{seconds:02d}")

        lines.append(f"Video ID: {data.metadata.video_id}")
        lines.append(f"Language: {data.language}")
        lines.append(f"Word Count: {data.word_count}")
        lines.append("")
        lines.append("─" * 60)
        lines.append("")
        lines.append(data.transcript)

        return "\n".join(lines)

    @staticmethod
    def format_markdown(data: TranscriptData) -> str:
        """Format as markdown with metadata and sections."""
        lines = []

        # Title
        if data.metadata.title:
            lines.append(f"# {data.metadata.title}")
            lines.append("")

        # Metadata table
        lines.append("## Video Info")
        lines.append("")
        lines.append("| Field | Value |")
        lines.append("|-------|-------|")

        if data.metadata.channel:
            lines.append(f"| Channel | {data.metadata.channel} |")
        if data.metadata.duration_seconds:
            minutes, seconds = divmod(data.metadata.duration_seconds, 60)
            lines.append(f"| Duration | {minutes}:{seconds:02d} |")

        lines.append(f"| Video ID | `{data.metadata.video_id}` |")
        lines.append(f"| Language | {data.language} |")
        lines.append(f"| Word Count | {data.word_count:,} |")

        video_url = f"https://www.youtube.com/watch?v={data.metadata.video_id}"
        lines.append(f"| URL | [{video_url}]({video_url}) |")
        lines.append("")

        # Transcript
        lines.append("## Transcript")
        lines.append("")
        lines.append(data.transcript)
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def format_json_data(data: TranscriptData) -> dict:
        """Format as dictionary for JSON output."""
        return {
            "video_id": data.metadata.video_id,
            "title": data.metadata.title,
            "channel": data.metadata.channel,
            "duration_seconds": data.metadata.duration_seconds,
            "thumbnail_url": data.metadata.thumbnail_url,
            "transcript": data.transcript,
            "word_count": data.word_count,
            "language": data.language,
        }
