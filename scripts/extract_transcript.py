#!/usr/bin/env python3
"""
LLD Transcript Extractor
Extracts Hindi auto-generated transcripts from YouTube videos
and formats them for note-taking.

Usage:
    .venv/bin/python scripts/extract_transcript.py <youtube_url> [--output path]
    .venv/bin/python scripts/extract_transcript.py --playlist <playlist_url>  # list all videos
"""

import sys
import re
import json
import subprocess
import argparse
from pathlib import Path


def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def get_video_info(video_id: str) -> dict:
    """Get video title and metadata via yt-dlp."""
    venv_bin = Path(__file__).parent.parent / ".venv" / "bin" / "yt-dlp"
    result = subprocess.run(
        [str(venv_bin), "--no-download", "-J", f"https://www.youtube.com/watch?v={video_id}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp failed: {result.stderr}")
    data = json.loads(result.stdout)
    return {
        "title": data.get("title", "Unknown"),
        "duration": data.get("duration", 0),
        "channel": data.get("channel", "Unknown"),
        "upload_date": data.get("upload_date", ""),
    }


def fetch_transcript(video_id: str) -> str:
    """Fetch transcript - tries English first, falls back to Hindi."""
    from youtube_transcript_api import YouTubeTranscriptApi

    ytt = YouTubeTranscriptApi()
    transcript_list = ytt.list(video_id)

    # Strategy 1: English auto-generated
    try:
        transcript = transcript_list.find_generated_transcript(["en"])
        entries = list(transcript.fetch())
        return format_transcript(entries)
    except Exception:
        pass

    # Strategy 2: English manual
    try:
        transcript = transcript_list.find_transcript(["en"])
        entries = list(transcript.fetch())
        return format_transcript(entries)
    except Exception:
        pass

    # Strategy 3: Hindi (auto-gen or manual) - return as-is
    # Hindi transcripts from this channel are actually Hinglish with many English terms
    try:
        transcript = transcript_list.find_transcript(["hi"])
        entries = list(transcript.fetch())
        return format_transcript(entries)
    except Exception:
        pass

    try:
        transcript = transcript_list.find_generated_transcript(["hi"])
        entries = list(transcript.fetch())
        return format_transcript(entries)
    except Exception:
        pass

    raise RuntimeError(f"No transcript available for video {video_id}")


def format_transcript(entries: list) -> str:
    """Format transcript entries into timestamped text."""
    lines = []
    for entry in entries:
        minutes = int(entry.start // 60)
        seconds = int(entry.start % 60)
        timestamp = f"{minutes}:{seconds:02d}"
        lines.append(f"{timestamp}\n{entry.text}")
    return "\n".join(lines)


def list_playlist(playlist_url: str):
    """List all videos in a playlist."""
    venv_bin = Path(__file__).parent.parent / ".venv" / "bin" / "yt-dlp"
    result = subprocess.run(
        [str(venv_bin), "--flat-playlist", "-J", playlist_url],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"yt-dlp failed: {result.stderr}")
    data = json.loads(result.stdout)
    
    print(f"Playlist: {data['title']}")
    print(f"Total videos: {len(data['entries'])}")
    print()
    for i, entry in enumerate(data['entries']):
        vid = entry['id']
        title = entry['title']
        url = f"https://www.youtube.com/watch?v={vid}"
        print(f"{i+1:2d}. {title}")
        print(f"    {url}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Extract YouTube transcript for LLD notes")
    parser.add_argument("url", nargs="?", help="YouTube video URL or video ID")
    parser.add_argument("--playlist", action="store_true", help="List all videos in playlist")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--raw", action="store_true", help="Output raw transcript without metadata header")
    args = parser.parse_args()

    if not args.url:
        parser.print_help()
        sys.exit(1)

    if args.playlist:
        list_playlist(args.url)
        return

    video_id = extract_video_id(args.url)
    
    # Get video info
    print(f"Fetching info for video: {video_id}...", file=sys.stderr)
    info = get_video_info(video_id)
    
    # Get transcript
    print(f"Fetching transcript...", file=sys.stderr)
    transcript = fetch_transcript(video_id)

    # Build output
    if args.raw:
        output = transcript
    else:
        duration_min = info['duration'] // 60
        duration_sec = info['duration'] % 60
        output = f"""# Transcript: {info['title']}

- **Video:** https://www.youtube.com/watch?v={video_id}
- **Channel:** {info['channel']}
- **Duration:** {duration_min}m {duration_sec}s
- **Language:** Hindi (auto-generated) — Hinglish with English tech terms

---

{transcript}
"""

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output)
        print(f"Saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
