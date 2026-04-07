"""Registry read/write operations for _tools/registry.json."""

from __future__ import annotations

import json
from datetime import datetime

from ayra_lib.config import IST, VaultConfig
from ayra_lib.types import ToolMeta, ToolRegistry


def load_registry(config: VaultConfig | None = None) -> ToolRegistry:
    """Load the tool registry from disk.

    Args:
        config: Vault configuration. Uses default if None.

    Returns:
        Parsed ToolRegistry snapshot.
    """
    cfg = config or VaultConfig()
    path = cfg.registry_path

    if not path.exists():
        return ToolRegistry(version="1.0.0", description="Empty registry")

    data = json.loads(path.read_text(encoding="utf-8"))

    tools = tuple(
        ToolMeta(
            name=t["name"],
            path=t.get("path", ""),
            version=t.get("version", "0.0.0"),
            runtime=t.get("runtime", "python"),
            description=t.get("description", ""),
            tags=tuple(t.get("tags", [])),
            status=t.get("status", "stable"),
            created=t.get("created", ""),
            tests=t.get("tests", ""),
        )
        for t in data.get("tools", [])
    )

    return ToolRegistry(
        version=data.get("version", "1.0.0"),
        description=data.get("description", ""),
        tools=tools,
        last_updated=data.get("last_updated", ""),
    )


def save_registry(registry: ToolRegistry, config: VaultConfig | None = None) -> None:
    """Write the tool registry to disk.

    Args:
        registry: The registry to persist.
        config: Vault configuration. Uses default if None.
    """
    cfg = config or VaultConfig()
    path = cfg.registry_path

    data = {
        "version": registry.version,
        "description": registry.description,
        "tools": [
            {
                "name": t.name,
                "path": t.path,
                "version": t.version,
                "runtime": t.runtime,
                "description": t.description,
                "tags": list(t.tags),
                "status": t.status,
                "created": t.created,
                "tests": t.tests,
            }
            for t in registry.tools
        ],
        "last_updated": datetime.now(IST).isoformat(),
    }

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
