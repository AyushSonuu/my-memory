# LangChain Integration Research

## Date: 2026-03-23

## Key Finding: Deep Agents SDK

LangChain now has three layers:
1. **LangChain** — core framework (models, tools, agents)
2. **LangGraph** — low-level orchestration runtime
3. **Deep Agents** — "agent harness" with VFS, memory, subagents, planning

Deep Agents is literally described as an "agent harness" — same concept as memharness.
It has: virtual filesystem, subagent-spawning, context management, memory persistence.

## Decision: Integration Strategy

memharness should NOT try to compete with Deep Agents. Instead:

### What memharness provides that Deep Agents doesn't:
- **10 typed memory categories** (conversational, knowledge, entity, workflow, etc.)
- **Pluggable backends** (PostgreSQL+pgvector, SQLite, in-memory)
- **Memory lifecycle management** (summarization, consolidation, GC)
- **Structured memory with schemas** per type
- **Framework-agnostic** — works with ANY agent framework, not just LangChain

### Integration approach:
1. **Tools**: Use `langchain-core` `BaseTool` for memory self-exploration tools
2. **Agents**: Use `langchain-core` `create_agent` for embedded memory agents (summarizer, consolidator, etc.)
3. **Memory adapter**: Implement LangChain's `BaseMemory` so any LangChain chain can use memharness
4. **Checkpointer**: Implement LangGraph's `BaseCheckpointSaver` for workflow state
5. **Deep Agents compatibility**: Provide a backend that Deep Agents can use for its memory

### Packages needed:
- `langchain-core>=0.3.0` — BaseTool, BaseMemory
- `langchain>=1.2.0` — create_agent (optional, for embedded agents)
- `langgraph>=0.3.0` — BaseCheckpointSaver (optional)

### Key primitives to use:
```python
from langchain_core.tools import BaseTool, tool  # For memory tools
from langchain_core.memory import BaseMemory      # For memory adapter
from langchain_core.runnables import Runnable      # For composability
```

## Source
- https://docs.langchain.com/oss/python/langchain/overview
- https://docs.langchain.com/oss/python/deepagents/overview
