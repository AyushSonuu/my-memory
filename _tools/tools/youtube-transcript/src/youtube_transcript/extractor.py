"""YouTube transcript extractor — video ID parsing, transcript fetching, metadata."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)

try:
    from pytubefix import YouTube
    PYTUBE_AVAILABLE = True
except ImportError:
    PYTUBE_AVAILABLE = False


@dataclass(frozen=True, slots=True)
class VideoMetadata:
    """Metadata for a YouTube video."""
    video_id: str
    title: str = ""
    channel: str = ""
    duration_seconds: int = 0
    thumbnail_url: str = ""


@dataclass(frozen=True, slots=True)
class TranscriptData:
    """Complete transcript data with metadata."""
    metadata: VideoMetadata
    transcript: str
    word_count: int
    language: str


class YouTubeExtractor:
    """Extracts transcripts and metadata from YouTube videos."""

    @staticmethod
    def extract_video_id(url: str) -> str | None:
        """Extract video ID from any YouTube URL format.

        Supports:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
        - https://www.youtube.com/v/VIDEO_ID
        - VIDEO_ID (11 characters)

        Returns:
            Video ID (11 chars) or None if invalid.
        """
        # Direct video ID (11 alphanumeric + underscore/hyphen)
        if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
            return url

        # Extract from various URL formats
        patterns = [
            r'(?:v=|/)([a-zA-Z0-9_-]{11}).*',  # watch?v= or /v/
            r'youtu\.be/([a-zA-Z0-9_-]{11})',   # youtu.be/
            r'embed/([a-zA-Z0-9_-]{11})',       # embed/
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    @staticmethod
    def fetch_metadata(video_id: str) -> VideoMetadata:
        """Fetch video metadata (title, channel, duration).

        Falls back to basic metadata if pytubefix is unavailable.
        """
        if not PYTUBE_AVAILABLE:
            return VideoMetadata(video_id=video_id)

        try:
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            return VideoMetadata(
                video_id=video_id,
                title=yt.title or "",
                channel=yt.author or "",
                duration_seconds=yt.length or 0,
                thumbnail_url=yt.thumbnail_url or "",
            )
        except Exception:
            # Fallback to basic metadata if fetch fails
            return VideoMetadata(video_id=video_id)

    @staticmethod
    def fetch_transcript(video_id: str, language: str = "en") -> tuple[str, str]:
        """Fetch transcript for a video.

        Args:
            video_id: YouTube video ID
            language: Preferred language code (e.g., 'en', 'hi')

        Returns:
            Tuple of (transcript_text, language_code)

        Raises:
            NoTranscriptFound: No transcript available
            TranscriptsDisabled: Transcripts disabled for this video
            VideoUnavailable: Video not found or unavailable
        """
        try:
            # Create API instance and fetch transcript
            api = YouTubeTranscriptApi()

            # Try with preferred language first, fallback to any available
            try:
                transcript = api.fetch(video_id, languages=[language])
            except NoTranscriptFound:
                # Try fetching with default (any available language)
                transcript = api.fetch(video_id)

            # Extract text from snippets
            text = " ".join(snippet.text for snippet in transcript.snippets)

            return text, transcript.language_code

        except (NoTranscriptFound, TranscriptsDisabled, VideoUnavailable) as e:
            raise e

    @classmethod
    def extract_full(
        cls,
        url: str | None = None,
        video_id: str | None = None,
        language: str = "en",
    ) -> TranscriptData:
        """Extract complete transcript data with metadata.

        Args:
            url: YouTube URL (if video_id not provided)
            video_id: YouTube video ID (if url not provided)
            language: Preferred language code

        Returns:
            Complete TranscriptData

        Raises:
            ValueError: If neither url nor video_id provided, or invalid
            NoTranscriptFound: No transcript available
            TranscriptsDisabled: Transcripts disabled
            VideoUnavailable: Video not found
        """
        if not url and not video_id:
            raise ValueError("Must provide either 'url' or 'video_id'")

        if url and video_id:
            raise ValueError("Provide only one of 'url' or 'video_id', not both")

        # Extract video ID from URL if needed
        if url:
            extracted_id = cls.extract_video_id(url)
            if not extracted_id:
                raise ValueError(f"Invalid YouTube URL: {url}")
            video_id = extracted_id

        # Validate video ID format
        if not video_id or not re.match(r'^[a-zA-Z0-9_-]{11}$', video_id):
            raise ValueError(f"Invalid YouTube video ID: {video_id}")

        # Fetch metadata and transcript
        metadata = cls.fetch_metadata(video_id)
        transcript_text, detected_language = cls.fetch_transcript(video_id, language)

        word_count = len(transcript_text.split())

        return TranscriptData(
            metadata=metadata,
            transcript=transcript_text,
            word_count=word_count,
            language=detected_language,
        )
