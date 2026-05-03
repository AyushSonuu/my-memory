"""Tests for YouTubeTranscriptTool."""

import pytest

from youtube_transcript.tool import YouTubeTranscriptTool


class TestToolSchema:
    """Test tool schema declaration."""

    def test_schema_has_required_fields(self):
        tool = YouTubeTranscriptTool()
        schema = tool.schema()

        assert schema.name == "youtube-transcript"
        assert schema.version == "1.0.0"
        assert len(schema.inputs) > 0
        assert len(schema.tags) > 0

    def test_schema_has_url_and_video_id_inputs(self):
        tool = YouTubeTranscriptTool()
        schema = tool.schema()

        input_names = {f.name for f in schema.inputs}
        assert "url" in input_names
        assert "video-id" in input_names
        assert "language" in input_names
        assert "format" in input_names


class TestToolValidation:
    """Test input validation."""

    def test_requires_url_or_video_id(self):
        tool = YouTubeTranscriptTool()
        result = tool.execute({})

        assert result.status.value == "error"
        assert "Must provide either" in result.message

    def test_not_both_url_and_video_id(self):
        tool = YouTubeTranscriptTool()
        result = tool.execute({
            "url": "https://www.youtube.com/watch?v=7AMjmCTumuo",
            "video-id": "7AMjmCTumuo",
        })

        assert result.status.value == "error"
        assert "only one" in result.message


class TestToolExecution:
    """Test tool execution (integration tests)."""

    @pytest.mark.integration
    def test_execute_with_url(self):
        """Integration test — requires network."""
        tool = YouTubeTranscriptTool()
        result = tool.execute({
            "url": "https://www.youtube.com/watch?v=7AMjmCTumuo"
        })

        assert result.status.value == "success"
        assert "video_id" in result.data
        assert result.data["video_id"] == "7AMjmCTumuo"
        assert "transcript" in result.data
        assert len(result.data["transcript"]) > 0

    @pytest.mark.integration
    def test_execute_with_video_id(self):
        """Integration test — requires network."""
        tool = YouTubeTranscriptTool()
        result = tool.execute({
            "video-id": "7AMjmCTumuo"
        })

        assert result.status.value == "success"
        assert result.data["video_id"] == "7AMjmCTumuo"
        assert len(result.data["transcript"]) > 0

    @pytest.mark.integration
    def test_execute_with_format_json(self):
        """Test JSON output format."""
        tool = YouTubeTranscriptTool()
        result = tool.execute({
            "video-id": "7AMjmCTumuo",
            "format": "json"
        })

        assert result.status.value == "success"
        assert isinstance(result.data, dict)
        assert "transcript" in result.data
