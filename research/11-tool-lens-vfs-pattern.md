# Tool Lens via VFS — Research for memharness

> Analysis of Ayush's SAP presentation on Virtual Filesystem for Tool Discovery

---

## Executive Summary

**Tool Lens via VFS** is a pattern developed at SAP (by Ayush Sanjeev Kumar) for **progressive tool discovery** in AI agents. Instead of loading 100+ tool schemas into context (50K tokens), it treats tools as files in a virtual filesystem that the agent can explore using familiar commands.

**This pattern should be adopted as the core design for memharness's Toolbox Memory.**

---

## 1. The Problem

### Context Window Bottleneck

```
Traditional Approach:
┌─────────────────────────────────────────┐
│  100+ MCP Tool Schemas = 50,000 tokens  │
│  ↓                                       │
│  Context filled before agent starts     │
│  ↓                                       │
│  Poor tool selection (60% accuracy)     │
│  High API costs, slow responses         │
│  No room for actual reasoning           │
└─────────────────────────────────────────┘
```

### Failed Approaches

| Approach | Problem | Success Rate |
|----------|---------|--------------|
| **Load All Tools** | 50K tokens, context overflow | 60% |
| **Simple Find & Execute** | 3-5 round trips, brittle | 95% but slow |

**Root Cause**: Context isolation — Tool Finder knows parameters, Assistant knows values. No bidirectional context sharing.

---

## 2. The VFS Solution

### Core Insight

> "Treat tools like files in a virtual filesystem. LLMs already know `ls`, `cat`, `grep`!"

### VFS Structure

```
/                           ← Root of tool filesystem
├── github/                 ← MCP Server = Directory
│   ├── list-issues.json    ← Tool = File (JSON schema)
│   ├── create-pr.json
│   └── merge-pr.json
├── slack/
│   ├── send-message.json
│   ├── list-channels.json
│   └── create-channel.json
├── sap-s4hana/
│   ├── get-material.json
│   └── create-order.json
└── salesforce/
    └── query-accounts.json
```

### 6 Familiar Operations

| Command | Action | Example |
|---------|--------|---------|
| `tree /` | Visualize entire VFS | See all servers + tool counts |
| `ls /slack/` | List directory | Show all Slack tools |
| `grep "message"` | Search across files | Find message-related tools |
| `cat tool.json` | Read file content | View complete schema |
| `glob */send*` | Pattern matching | Find all 'send' tools |
| `select [tools]` | Load into context | Finalize selection |

---

## 3. ReAct Discovery Flow

### Example: "Send a Slack message about Q4 results"

```
Step 1: Think → "User wants to send to Slack. Explore Slack server."
        Action → tree /
        Result → Found: /github/, /slack/, /sap/, /salesforce/

Step 2: Think → "Found slack. What message tools available?"
        Action → ls /slack/
        Result → send-message.json, list-channels.json, create-channel.json

Step 3: Think → "send-message.json looks right. Check schema."
        Action → cat /slack/send-message.json
        Result → Schema: {channel: string, text: string, blocks: array}

Step 4: Think → "This matches! User needs to send a message."
        Action → select ["/slack/send-message.json"]
        Result → SUCCESS - Tool found in 4 iterations, ~2K tokens
```

**Result**: Tool found in 4 iterations | 2,000 tokens vs 50,000 (96% savings)

---

## 4. State Machine Architecture

```
           ┌──────────┐
           │ __start__│
           └────┬─────┘
                ▼
           ┌──────────┐
           │  router  │
           └────┬─────┘
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
  ┌─────────┐ ┌───────┐ ┌─────────┐
  │discover │ │decide │ │ execute │
  └────┬────┘ └───┬───┘ └────┬────┘
       │          │          │
       └──────────┼──────────┘
                  ▼
            ┌──────────┐
            │  clarify │
            └────┬─────┘
                 ▼
            ┌──────────┐
            │ __end__  │
            └──────────┘
```

**Modes**:
- **Discover**: Explore VFS, find candidate tools
- **Decide**: Evaluate candidates, narrow selection
- **Execute**: Run selected tool with parameters
- **Clarify**: Ask user for missing information

---

## 5. Production Metrics

| Metric | Before VFS | With VFS | Improvement |
|--------|------------|----------|-------------|
| **Tokens for tools** | 75,000 | 500 | **99% reduction** |
| **Simple success** | 85% | 95% | +10% |
| **Complex success** | 20% | 85% | **+65%** |
| **Multi-turn** | No | Yes (robust) | New capability |
| **Avg turns** | N/A | 1.8 | Efficient |
| **Cost** | Baseline | 10x savings | **10x** |

**Scales to 10,000+ tools efficiently!**

---

## 6. How This Fits in memharness

### 6.1 Toolbox Memory = VFS Pattern

memharness's **Toolbox Memory** should implement this exact pattern:

```python
class ToolboxMemory:
    """VFS-based tool discovery for memharness."""

    async def tree(self, path: str = "/") -> str:
        """Visualize tool hierarchy."""
        ...

    async def ls(self, path: str) -> list[str]:
        """List tools in a server/directory."""
        ...

    async def grep(self, pattern: str, path: str = "/") -> list[dict]:
        """Search tools by pattern (semantic + keyword)."""
        ...

    async def cat(self, tool_path: str) -> dict:
        """Get full tool schema."""
        ...

    async def glob(self, pattern: str) -> list[str]:
        """Pattern matching for tools."""
        ...

    async def select(self, tool_paths: list[str]) -> list[dict]:
        """Load selected tools into context."""
        ...
```

### 6.2 Integration with Memory Harness

```python
from memharness import MemoryHarness

memory = MemoryHarness(backend="postgresql://...")

# Register MCP tools via VFS
memory.toolbox.register_server("github", github_mcp_tools)
memory.toolbox.register_server("slack", slack_mcp_tools)
memory.toolbox.register_server("sap", sap_mcp_tools)

# Agent uses VFS operations
tools = await memory.toolbox.grep("send message")
schema = await memory.toolbox.cat("/slack/send-message.json")
selected = await memory.toolbox.select(["/slack/send-message.json"])

# Or get VFS tools for agent to use directly
vfs_tools = memory.toolbox.get_discovery_tools()
agent = YourAgent(tools=vfs_tools)
```

### 6.3 Extended VFS for All Memory Types

The VFS pattern can extend beyond toolbox:

```
/                           ← Root of memory filesystem
├── toolbox/                ← Tool schemas (original VFS)
│   ├── github/
│   └── slack/
├── knowledge/              ← Knowledge base documents
│   ├── arxiv/
│   └── docs/
├── workflows/              ← Workflow patterns
│   ├── common/
│   └── user/
├── skills/                 ← Learned capabilities
│   ├── coding/
│   └── analysis/
└── entities/               ← Entity memory
    ├── people/
    └── organizations/
```

This gives a **unified exploration interface** for all memory types!

---

## 7. Key Takeaways for memharness

| Insight | Application |
|---------|-------------|
| VFS abstraction intuitive | Use for Toolbox Memory |
| Treat tools like files | Leverage LLM training on filesystems |
| Progressive loading | Don't load all at once |
| ReAct pattern | Enable intelligent exploration |
| Multi-turn state | Persist discovery context |
| 96% token savings | Major cost reduction |
| Scales to 10K+ | Enterprise-ready |

---

## 8. Updated Toolbox Memory Design

### Schema

```python
@dataclass
class ToolboxEntry:
    server: str           # e.g., "github", "slack"
    tool_name: str        # e.g., "send-message"
    description: str      # Human-readable description
    schema: dict          # Full JSON schema
    embedding: list[float]  # For semantic search
    path: str             # VFS path: "/slack/send-message.json"
    metadata: dict        # Tags, usage count, etc.
```

### Storage

```sql
CREATE TABLE toolbox_memory (
    id UUID PRIMARY KEY,
    server VARCHAR(255) NOT NULL,
    tool_name VARCHAR(255) NOT NULL,
    description TEXT,
    schema JSONB NOT NULL,
    embedding vector(768),
    path VARCHAR(512) UNIQUE NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_toolbox_server ON toolbox_memory(server);
CREATE INDEX idx_toolbox_path ON toolbox_memory(path);
CREATE INDEX idx_toolbox_embedding ON toolbox_memory USING hnsw(embedding vector_cosine_ops);
```

### Operations Mapping

| VFS Command | memharness Implementation |
|-------------|--------------------------|
| `tree /` | `toolbox.list_servers()` |
| `ls /slack/` | `toolbox.list_tools(server="slack")` |
| `grep "msg"` | `toolbox.search(query="msg")` (semantic) |
| `cat /slack/send.json` | `toolbox.get_schema(path)` |
| `glob */send*` | `toolbox.glob_search(pattern)` |
| `select [...]` | `toolbox.load_tools(paths)` |

---

## 9. Recommendation

**Adopt the VFS pattern as a first-class feature in memharness:**

1. ✅ Implement for Toolbox Memory (primary use case)
2. ✅ Extend to other memory types (knowledge, skills, workflows)
3. ✅ Provide VFS discovery tools for agents
4. ✅ Support semantic search within VFS (`grep` with embeddings)
5. ✅ Add usage tracking for tool popularity

This aligns perfectly with the **"Toolbox Pattern"** from the DeepLearning.AI course you studied!

---

## Source

- **Tool Lens via VFS** presentation by Ayush Sanjeev Kumar (SAP)
- SAP dCom Developers League

---

*Research completed: 2026-03-22*
