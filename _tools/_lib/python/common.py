"""
Shared Python utilities for _tools/.
Import from here to avoid duplication across tools.
"""

import json
import yaml
import os
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

# IST timezone
IST = timezone(timedelta(hours=5, minutes=30))

# Repo root (two levels up from _lib/python/)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOOLS_ROOT = REPO_ROOT / "_tools"
TECH_ROOT = REPO_ROOT / "tech"


def load_registry() -> dict:
    """Load the tools registry."""
    registry_path = TOOLS_ROOT / "registry.json"
    with open(registry_path) as f:
        return json.load(f)


def load_tool_yaml(tool_name: str) -> dict:
    """Load a tool's metadata from tool.yaml."""
    tool_path = TOOLS_ROOT / tool_name / "tool.yaml"
    with open(tool_path) as f:
        return yaml.safe_load(f)


def find_topic_path(topic_name: str) -> Path | None:
    """Find a topic folder by name under tech/."""
    # Direct match
    direct = TECH_ROOT / topic_name
    if direct.is_dir():
        return direct
    
    # Search recursively (for nested topics like python/asyncio)
    for p in TECH_ROOT.rglob("*"):
        if p.is_dir() and p.name == topic_name:
            return p
    return None


def now_ist() -> datetime:
    """Current time in IST."""
    return datetime.now(IST)


def timestamp_ist() -> str:
    """ISO timestamp in IST."""
    return now_ist().isoformat()
