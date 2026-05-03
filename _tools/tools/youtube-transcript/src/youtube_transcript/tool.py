"""YouTubeTranscriptTool — BaseTool implementation."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from ayra_lib.tool_interface import (
    BaseTool,
    InputField,
    ToolOutput,
    ToolSchema,
    ToolStatus,
)
from youtube_transcript.extractor import YouTubeExtractor
from youtube_transcript.formatter import TranscriptFormatter
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)


class YouTubeTranscriptTool(BaseTool):
    """Extract transcripts from YouTube videos."""

    VERSION = "1.0.0"

    def schema(self) -> ToolSchema:
        """Declare input/output schema."""
        return ToolSchema(
            name="youtube-transcript",
            version=self.VERSION,
            description="Extract transcripts from YouTube videos for note-taking and vault ingestion.",
            inputs=(
                InputField(
                    name="url",
                    type="string",
                    required=False,
                    description="Full YouTube URL (any format: watch?v=, youtu.be/, embed/, etc.)",
                ),
                InputField(
                    name="video-id",
                    type="string",
                    required=False,
                    description="YouTube video ID (11 characters, e.g., '7AMjmCTumuo')",
                ),
                InputField(
                    name="language",
                    type="string",
                    required=False,
                    default="en",
                    description="Preferred language code (e.g., 'en', 'hi', 'es')",
                ),
                InputField(
                    name="format",
                    type="string",
                    required=False,
                    default="text",
                    enum=("text", "json", "markdown"),
                    description="Output format: text, json, or markdown",
                ),
                InputField(
                    name="output",
                    type="string",
                    required=False,
                    description="Optional file path to save transcript",
                ),
            ),
            output_description="Transcript data with metadata (video_id, title, channel, transcript, word_count, language)",
            tags=("youtube", "transcript", "ingest", "video", "learning"),
            examples=(
                {"url": "https://www.youtube.com/watch?v=7AMjmCTumuo"},
                {"video-id": "7AMjmCTumuo", "language": "en"},
                {"url": "https://youtu.be/7AMjmCTumuo", "format": "markdown", "output": "transcript.md"},
            ),
        )

    def execute(self, inputs: dict[str, Any]) -> ToolOutput:
        """Execute transcript extraction programmatically."""
        url = inputs.get("url")
        video_id = inputs.get("video-id")
        language = inputs.get("language", "en")
        output_format = inputs.get("format", "text")
        output_path = inputs.get("output")

        # Validation: must provide exactly one of url or video-id
        if not url and not video_id:
            return self._make_error("Must provide either 'url' or 'video-id'")

        if url and video_id:
            return self._make_error("Provide only one of 'url' or 'video-id', not both")

        # Extract transcript
        try:
            data = YouTubeExtractor.extract_full(
                url=url,
                video_id=video_id,
                language=language,
            )
        except ValueError as e:
            return self._make_error(str(e))
        except VideoUnavailable:
            vid = video_id or url
            return self._make_error(f"Video not found or unavailable: {vid}")
        except (NoTranscriptFound, TranscriptsDisabled):
            vid = video_id or url
            return self._make_error(f"No transcript available for video: {vid}")
        except Exception as e:
            return self._make_error(f"Failed to fetch transcript: {e}")

        # Format output
        if output_format == "json":
            formatted = TranscriptFormatter.format_json_data(data)
        elif output_format == "markdown":
            formatted = TranscriptFormatter.format_markdown(data)
        else:  # text
            formatted = TranscriptFormatter.format_text(data)

        # Save to file if requested
        if output_path:
            try:
                Path(output_path).write_text(
                    formatted if isinstance(formatted, str) else str(formatted),
                    encoding="utf-8",
                )
            except Exception as e:
                return self._make_error(f"Failed to write output file: {e}")

        # Build response
        if output_format == "json":
            result_data = formatted
        else:
            result_data = TranscriptFormatter.format_json_data(data)

        # Duration formatting for message
        duration_str = ""
        if data.metadata.duration_seconds:
            minutes, seconds = divmod(data.metadata.duration_seconds, 60)
            duration_str = f" ({minutes}:{seconds:02d})"

        title = data.metadata.title or data.metadata.video_id
        message = f"Extracted transcript from '{title}'{duration_str}"

        if output_path:
            message += f" → saved to {output_path}"

        return ToolOutput(
            status=ToolStatus.SUCCESS,
            tool="youtube-transcript",
            version=self.VERSION,
            data=result_data,
            message=message,
        )

    def run_interactive(self, inputs: dict[str, Any]) -> None:
        """Run in interactive mode with pretty terminal output."""
        result = self.execute(inputs)

        if result.status == ToolStatus.ERROR:
            print(f"❌ {result.message}", file=sys.stderr)
            for err in result.errors:
                print(f"   {err}", file=sys.stderr)
            sys.exit(1)

        # Display success message
        print(f"✅ {result.message}")
        print()

        # Display transcript (formatted based on user's choice)
        output_format = inputs.get("format", "text")
        output_path = inputs.get("output")

        if output_path:
            print(f"📄 Transcript saved to: {output_path}")
        else:
            # Display inline
            if output_format == "json":
                import json
                print(json.dumps(result.data, indent=2, ensure_ascii=False))
            elif output_format == "markdown":
                # Read back from data
                url = inputs.get("url")
                video_id = inputs.get("video-id") or YouTubeExtractor.extract_video_id(url or "")
                language = inputs.get("language", "en")

                data = YouTubeExtractor.extract_full(
                    url=url,
                    video_id=video_id,
                    language=language,
                )
                print(TranscriptFormatter.format_markdown(data))
            else:  # text
                url = inputs.get("url")
                video_id = inputs.get("video-id") or YouTubeExtractor.extract_video_id(url or "")
                language = inputs.get("language", "en")

                data = YouTubeExtractor.extract_full(
                    url=url,
                    video_id=video_id,
                    language=language,
                )
                print(TranscriptFormatter.format_text(data))
