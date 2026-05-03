"""Tests for YouTube extractor."""

import pytest

from youtube_transcript.extractor import YouTubeExtractor


class TestVideoIDExtraction:
    """Test video ID extraction from various URL formats."""

    def test_extract_from_watch_url(self):
        url = "https://www.youtube.com/watch?v=7AMjmCTumuo"
        assert YouTubeExtractor.extract_video_id(url) == "7AMjmCTumuo"

    def test_extract_from_short_url(self):
        url = "https://youtu.be/7AMjmCTumuo"
        assert YouTubeExtractor.extract_video_id(url) == "7AMjmCTumuo"

    def test_extract_from_embed_url(self):
        url = "https://www.youtube.com/embed/7AMjmCTumuo"
        assert YouTubeExtractor.extract_video_id(url) == "7AMjmCTumuo"

    def test_extract_direct_video_id(self):
        video_id = "7AMjmCTumuo"
        assert YouTubeExtractor.extract_video_id(video_id) == "7AMjmCTumuo"

    def test_extract_with_playlist(self):
        url = "https://www.youtube.com/watch?v=7AMjmCTumuo&list=PL-osiE80TeTsak-c-QsVeg0YYG_0TeyXI"
        assert YouTubeExtractor.extract_video_id(url) == "7AMjmCTumuo"

    def test_invalid_url_returns_none(self):
        assert YouTubeExtractor.extract_video_id("not-a-youtube-url") is None
        assert YouTubeExtractor.extract_video_id("https://vimeo.com/123") is None
        assert YouTubeExtractor.extract_video_id("") is None


class TestTranscriptExtraction:
    """Test transcript fetching (requires network)."""

    @pytest.mark.integration
    def test_fetch_transcript_success(self):
        """Integration test — requires network and valid video."""
        video_id = "7AMjmCTumuo"  # Corey Schafer threading video
        text, lang = YouTubeExtractor.fetch_transcript(video_id)

        assert len(text) > 0
        assert lang in ["en", "en-US", "en-GB"]

    @pytest.mark.integration
    def test_extract_full_with_url(self):
        """Integration test — full extraction."""
        url = "https://www.youtube.com/watch?v=7AMjmCTumuo"
        data = YouTubeExtractor.extract_full(url=url)

        assert data.metadata.video_id == "7AMjmCTumuo"
        assert len(data.transcript) > 0
        assert data.word_count > 0
        assert data.language.startswith("en")

    def test_extract_full_requires_url_or_id(self):
        """Must provide at least one of url or video_id."""
        with pytest.raises(ValueError, match="Must provide either"):
            YouTubeExtractor.extract_full()

    def test_extract_full_not_both(self):
        """Cannot provide both url and video_id."""
        with pytest.raises(ValueError, match="only one"):
            YouTubeExtractor.extract_full(
                url="https://www.youtube.com/watch?v=7AMjmCTumuo",
                video_id="7AMjmCTumuo",
            )
