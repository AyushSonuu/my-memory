# AI-Native Memory Management — Embedded Agent Architecture

> Specialized AI agents that autonomously manage all memory operations within memharness

---

## Important: Deterministic-First Principle

**Simple operations are DETERMINISTIC (no AI needed). AI agents only handle complex tasks.**

```
DETERMINISTIC (Direct, No AI)          AI-ASSISTED (Agents Required)
─────────────────────────────────      ─────────────────────────────────
memory.add_conversational() → Direct   memory.add() (no type) → Router
memory.add_entity() → Direct           Entity extraction → LLM needed
memory.get_*() → Direct                Summarization → LLM needed
memory.search_*() → Direct             Consolidation → LLM needed
memory.expand_summary() → Direct       Context assembly → LLM needed
```

---

## Executive Summary

memharness should have **embedded AI agents** that autonomously handle memory management tasks — not as optional add-ons, but as **core infrastructure**. These agents run deterministically (scheduled or policy-triggered) and require minimal human intervention.

**Philosophy**: Memory management is too complex for static rules. Let specialized AI agents handle it.

---

## 1. The Vision: AI-Managed Memory Infrastructure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              memharness                                      │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                    EMBEDDED AI AGENT LAYER                              ││
│  │                                                                         ││
│  │   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     ││
│  │   │  🗂️ Router  │ │ 🔄 Consol. │ │ 📝 Summary │ │ 🏷️ Entity  │     ││
│  │   │   Agent     │ │   Agent     │ │   Agent     │ │  Extractor  │     ││
│  │   └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘     ││
│  │   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     ││
│  │   │ 🗑️ GC      │ │ 🔍 Tool    │ │ 📋 Context │ │ 🔧 Index   │     ││
│  │   │   Agent     │ │  Discovery  │ │  Assembler  │ │  Optimizer  │     ││
│  │   └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘     ││
│  │                                                                         ││
│  │   All agents run autonomously based on policies and triggers           ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                      │                                       │
│  ┌───────────────────────────────────┴──────────────────────────────────┐   │
│  │                        Memory Manager                                 │   │
│  │                     (CRUD + Type Registry)                           │   │
│  └───────────────────────────────────┬──────────────────────────────────┘   │
│                                      │                                       │
│  ┌───────────────────────────────────┴──────────────────────────────────┐   │
│  │                        Storage Layer                                  │   │
│  │              (PostgreSQL | SQLite | Redis | Memory)                  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. The 8 Specialized Memory Agents

### 2.1 Memory Router Agent 🗂️

**Purpose**: Intelligently route incoming memories to the correct type and storage.

**When it runs**: On every `memory.add()` call (synchronous)

**What it does**:
- Analyzes content to determine memory type (if not specified)
- Decides storage tier (hot/warm/cold)
- Applies namespace routing rules
- Handles cross-type relationships

```python
class MemoryRouterAgent(EmbeddedAgent):
    """Routes memories to correct stores based on content analysis."""

    trigger = TriggerType.ON_WRITE  # Runs on every write

    async def process(self, content: str, metadata: dict) -> RoutingDecision:
        # Analyze content
        analysis = await self.llm.analyze(f"""
        Classify this content into memory type and determine routing:

        Content: {content}
        Metadata: {metadata}

        Memory Types: conversational, knowledge_base, entity, workflow,
                     toolbox, summary, tool_log, skills, file, persona

        Return: {{
            "memory_type": "...",
            "storage_tier": "hot|warm|cold",
            "namespace_suggestion": [...],
            "related_types": [...],
            "confidence": 0.0-1.0
        }}
        """)

        return RoutingDecision(**analysis)
```

### 2.2 Consolidation Agent 🔄

**Purpose**: Merge duplicate/similar memories, maintain consistency.

**When it runs**:
- Scheduled (e.g., daily at 3 AM)
- When similarity threshold exceeded on write

**What it does**:
- Finds semantically similar memories
- Merges duplicates intelligently
- Resolves conflicts (newer wins, or merge)
- Updates references

```python
class ConsolidationAgent(EmbeddedAgent):
    """Merges duplicate memories and maintains consistency."""

    trigger = TriggerType.SCHEDULED
    schedule = "0 3 * * *"  # Daily at 3 AM

    async def run(self, memory_type: str = "*"):
        # Find clusters of similar memories
        clusters = await self._find_similar_clusters(memory_type)

        for cluster in clusters:
            if cluster.similarity > 0.9:
                # Merge into single memory
                merged = await self._merge_memories(cluster.memories)
                await self.memory.write(merged)
                await self.memory.delete_batch(cluster.memory_ids)

                self.log(f"Merged {len(cluster.memories)} memories → {merged.id}")

    async def _merge_memories(self, memories: list) -> MemoryUnit:
        """Use LLM to intelligently merge memories."""
        merged_content = await self.llm.generate(f"""
        Merge these related memories into a single, comprehensive memory:

        {[m.content for m in memories]}

        Rules:
        - Preserve all unique information
        - Resolve contradictions (prefer most recent)
        - Create a coherent, deduplicated result
        """)
        return MemoryUnit(content=merged_content, ...)
```

### 2.3 Summarization Agent 📝

**Purpose**: Compress old memories while preserving important information.

**When it runs**:
- When context window exceeds threshold (e.g., 80%)
- When conversation age exceeds threshold (e.g., 7 days)
- Before archival

**What it does**:
- Summarizes old conversations
- Creates summary memories with source links
- Marks original memories as summarized
- Supports expansion (summary → original)

```python
class SummarizationAgent(EmbeddedAgent):
    """Compresses old memories into summaries."""

    trigger = TriggerType.POLICY
    policies = [
        Policy(memory_type="conversational", condition="age > 7d", action="summarize"),
        Policy(memory_type="*", condition="context_usage > 80%", action="summarize"),
    ]

    async def summarize_conversation(self, thread_id: str) -> str:
        # Get conversation history
        messages = await self.memory.read_conversational(thread_id, limit=100)

        # Generate summary
        summary = await self.llm.generate(f"""
        Summarize this conversation, preserving:
        - Key decisions made
        - Important facts mentioned
        - User preferences expressed
        - Action items or commitments

        Conversation:
        {messages}
        """)

        # Store summary
        summary_id = await self.memory.write_summary(
            summary=summary,
            source_ids=[m.id for m in messages],
            thread_id=thread_id,
        )

        # Mark originals as summarized
        await self._mark_summarized(messages, summary_id)

        return summary_id
```

### 2.4 Entity Extraction Agent 🏷️

**Purpose**: Extract structured entities from unstructured content.

**When it runs**:
- On every conversational memory write
- On knowledge base additions
- Batch processing of existing memories

**What it does**:
- Extracts people, organizations, places, concepts
- Creates/updates entity memories
- Builds relationship graph
- Maintains entity consistency

```python
class EntityExtractionAgent(EmbeddedAgent):
    """Extracts structured entities from content."""

    trigger = TriggerType.ON_WRITE
    applies_to = ["conversational", "knowledge_base"]

    async def extract(self, content: str, namespace: tuple) -> list[Entity]:
        entities = await self.llm.generate(f"""
        Extract all entities from this content:

        {content}

        For each entity, provide:
        - name: The entity name
        - type: PERSON | ORGANIZATION | PLACE | CONCEPT | SYSTEM | PRODUCT
        - description: Brief description based on context
        - relationships: Any relationships to other entities

        Return as JSON array.
        """)

        # Store each entity
        for entity in entities:
            existing = await self.memory.search_entity(
                query=entity.name,
                namespace=namespace,
                k=1,
            )

            if existing and existing[0].similarity > 0.95:
                # Update existing entity
                await self._merge_entity(existing[0], entity)
            else:
                # Create new entity
                await self.memory.write_entity(**entity, namespace=namespace)

        return entities
```

### 2.5 Garbage Collection Agent 🗑️

**Purpose**: Remove stale, expired, and orphaned memories.

**When it runs**:
- Scheduled (e.g., weekly)
- When storage exceeds threshold
- On explicit trigger

**What it does**:
- Removes expired memories (TTL)
- Cleans up orphaned references
- Archives old data to cold storage
- Reclaims storage space

```python
class GCAgent(EmbeddedAgent):
    """Garbage collection for stale memories."""

    trigger = TriggerType.SCHEDULED
    schedule = "0 4 * * 0"  # Weekly on Sunday at 4 AM

    async def run(self):
        stats = {"deleted": 0, "archived": 0, "orphans_cleaned": 0}

        # 1. Delete expired memories
        expired = await self.memory.list(
            filters={"expires_at": {"$lt": datetime.utcnow()}}
        )
        for mem in expired:
            await self.memory.delete(mem.id)
            stats["deleted"] += 1

        # 2. Archive old memories (move to cold storage)
        old = await self.memory.list(
            filters={"created_at": {"$lt": datetime.utcnow() - timedelta(days=90)}}
        )
        for mem in old:
            await self._archive(mem)
            stats["archived"] += 1

        # 3. Clean orphaned references
        orphans = await self._find_orphaned_references()
        for orphan in orphans:
            await self._clean_orphan(orphan)
            stats["orphans_cleaned"] += 1

        # 4. Optimize storage
        await self._vacuum_storage()

        self.log(f"GC complete: {stats}")
        return stats
```

### 2.6 Tool Discovery Agent 🔍 (VFS-based)

**Purpose**: Progressive tool discovery using VFS pattern.

**When it runs**:
- On user query that needs tools
- When agent requests tool discovery

**What it does**:
- Explores tool VFS using ReAct pattern
- Finds relevant tools efficiently
- Returns only needed schemas
- Learns from successful discoveries

```python
class ToolDiscoveryAgent(EmbeddedAgent):
    """VFS-based progressive tool discovery (Tool Lens pattern)."""

    trigger = TriggerType.ON_DEMAND

    async def discover(self, intent: str) -> list[dict]:
        """
        Discover tools for given intent using VFS exploration.

        Example: "Send a Slack message" → [slack/send-message.json]
        """
        messages = [
            {"role": "system", "content": TOOL_DISCOVERY_PROMPT},
            {"role": "user", "content": f"Find tools for: {intent}"},
        ]

        tools = [
            self.vfs_tree,
            self.vfs_ls,
            self.vfs_grep,
            self.vfs_cat,
            self.vfs_glob,
            self.vfs_select,
        ]

        # ReAct loop
        for _ in range(MAX_ITERATIONS):
            response = await self.llm.generate(messages, tools=tools)

            if response.tool_calls:
                for tc in response.tool_calls:
                    result = await self._execute_vfs_op(tc)
                    messages.append({"role": "tool", "content": result})
            else:
                # Final answer - selected tools
                return self._parse_selected_tools(response.content)

        return []
```

### 2.7 Context Assembly Agent 📋

**Purpose**: Build optimal context windows for LLM calls.

**When it runs**:
- Before every LLM invocation
- On context refresh requests

**What it does**:
- Retrieves relevant memories per type
- Prioritizes based on relevance and recency
- Manages token budget
- Formats for LLM consumption

```python
class ContextAssemblyAgent(EmbeddedAgent):
    """Assembles optimal context from memory."""

    trigger = TriggerType.ON_DEMAND

    async def assemble(
        self,
        query: str,
        thread_id: str,
        max_tokens: int = 4000,
    ) -> str:
        """
        Assemble context window with priority-based allocation.

        Returns formatted markdown with memory sections.
        """
        budget = TokenBudget(max_tokens)
        context_parts = []

        # Priority 1: Recent conversation (40% budget)
        conv = await self.memory.read_conversational(
            thread_id,
            limit=self._tokens_to_messages(budget.allocate(0.4))
        )
        context_parts.append(("## Conversation Memory", conv))

        # Priority 2: Relevant knowledge (30% budget)
        kb = await self.memory.search_knowledge_base(
            query,
            k=self._tokens_to_docs(budget.allocate(0.3))
        )
        context_parts.append(("## Knowledge Base Memory", kb))

        # Priority 3: Entities (15% budget)
        entities = await self.memory.search_entity(
            query,
            k=self._tokens_to_entities(budget.allocate(0.15))
        )
        context_parts.append(("## Entity Memory", entities))

        # Priority 4: Workflows (10% budget)
        workflows = await self.memory.search_workflow(
            query,
            k=self._tokens_to_workflows(budget.allocate(0.10))
        )
        context_parts.append(("## Workflow Memory", workflows))

        # Priority 5: Summaries (5% budget)
        summaries = await self.memory.read_summary_context(
            query,
            thread_id=thread_id
        )
        context_parts.append(("## Summary Memory", summaries))

        return self._format_context(context_parts)
```

### 2.8 Index Optimization Agent 🔧

**Purpose**: Maintain search performance and index health.

**When it runs**:
- Scheduled (e.g., weekly)
- When query latency exceeds threshold
- After bulk writes

**What it does**:
- Rebuilds degraded indexes
- Optimizes vector indexes (rebalance HNSW)
- Updates statistics for query planner
- Monitors and reports performance

```python
class IndexOptimizationAgent(EmbeddedAgent):
    """Maintains search index performance."""

    trigger = TriggerType.SCHEDULED
    schedule = "0 5 * * 0"  # Weekly on Sunday at 5 AM

    async def run(self):
        stats = {}

        for memory_type in self.memory.list_types():
            config = self.memory.get_type_config(memory_type)

            if config.index_type == "hnsw":
                # Check index health
                health = await self._check_hnsw_health(memory_type)

                if health.fragmentation > 0.3:
                    # Rebuild index
                    await self._rebuild_hnsw_index(memory_type)
                    stats[memory_type] = "rebuilt"
                else:
                    stats[memory_type] = "healthy"

            elif config.storage == "sql":
                # Update statistics
                await self._update_sql_statistics(memory_type)
                stats[memory_type] = "stats_updated"

        # Vacuum if needed
        if await self._should_vacuum():
            await self._vacuum_database()

        self.log(f"Index optimization complete: {stats}")
        return stats
```

---

## 3. Agent Coordination & Orchestration

### 3.1 Agent Scheduler

```python
class AgentScheduler:
    """Coordinates all embedded agents."""

    def __init__(self, memory: MemoryHarness, llm: LLMProvider):
        self.memory = memory
        self.llm = llm
        self.agents = self._init_agents()
        self.scheduler = AsyncIOScheduler()

    def _init_agents(self) -> dict[str, EmbeddedAgent]:
        return {
            "router": MemoryRouterAgent(self.memory, self.llm),
            "consolidation": ConsolidationAgent(self.memory, self.llm),
            "summarization": SummarizationAgent(self.memory, self.llm),
            "entity_extraction": EntityExtractionAgent(self.memory, self.llm),
            "gc": GCAgent(self.memory, self.llm),
            "tool_discovery": ToolDiscoveryAgent(self.memory, self.llm),
            "context_assembly": ContextAssemblyAgent(self.memory, self.llm),
            "index_optimization": IndexOptimizationAgent(self.memory, self.llm),
        }

    async def start(self):
        """Start all scheduled agents."""
        for name, agent in self.agents.items():
            if agent.trigger == TriggerType.SCHEDULED:
                self.scheduler.add_job(
                    agent.run,
                    CronTrigger.from_crontab(agent.schedule),
                    id=name,
                )
        self.scheduler.start()

    async def run_agent(self, name: str, **kwargs):
        """Manually trigger an agent."""
        return await self.agents[name].run(**kwargs)
```

### 3.2 Event-Driven Triggers

```python
class EventBus:
    """Event bus for agent triggers."""

    async def emit(self, event: str, data: dict):
        """Emit event to trigger agents."""

        if event == "memory.write":
            # Trigger router and entity extraction
            await self.agents["router"].process(data["content"], data["metadata"])
            await self.agents["entity_extraction"].extract(data["content"], data["namespace"])

        elif event == "context.threshold":
            # Trigger summarization
            await self.agents["summarization"].summarize_conversation(data["thread_id"])

        elif event == "tool.request":
            # Trigger tool discovery
            return await self.agents["tool_discovery"].discover(data["intent"])

        elif event == "context.assemble":
            # Trigger context assembly
            return await self.agents["context_assembly"].assemble(**data)
```

---

## 4. Deterministic Operation Modes

### 4.1 Operation Matrix

| Agent | Deterministic | Agent-Triggered | User-Triggered |
|-------|--------------|-----------------|----------------|
| **Router** | ✅ On every write | - | - |
| **Entity Extractor** | ✅ On every write | - | - |
| **Context Assembler** | ✅ Before LLM call | - | - |
| **Summarization** | ✅ Policy-based | ✅ On threshold | ✅ Manual |
| **Consolidation** | ✅ Scheduled | - | ✅ Manual |
| **GC** | ✅ Scheduled | - | ✅ Manual |
| **Index Optimizer** | ✅ Scheduled | ✅ On degradation | ✅ Manual |
| **Tool Discovery** | - | ✅ On request | - |

### 4.2 Deterministic Guarantees

```python
class DeterministicPolicy:
    """Ensures deterministic agent behavior."""

    # Always run these on write
    ON_WRITE_AGENTS = ["router", "entity_extraction"]

    # Always run these before LLM
    PRE_LLM_AGENTS = ["context_assembly"]

    # Always run these post-LLM
    POST_LLM_AGENTS = ["entity_extraction"]  # On response

    # Scheduled (cron-based)
    SCHEDULED_AGENTS = {
        "consolidation": "0 3 * * *",   # Daily 3 AM
        "gc": "0 4 * * 0",              # Weekly Sunday 4 AM
        "index_optimizer": "0 5 * * 0", # Weekly Sunday 5 AM
    }

    # Policy-triggered
    POLICY_AGENTS = {
        "summarization": [
            {"condition": "age > 7d", "memory_type": "conversational"},
            {"condition": "context_usage > 80%", "memory_type": "*"},
        ],
    }
```

---

## 5. LLM Provider Abstraction

```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """Abstract LLM provider for embedded agents."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        tools: list[dict] = None,
        **kwargs,
    ) -> str:
        """Generate completion."""
        ...

    @abstractmethod
    async def analyze(self, prompt: str) -> dict:
        """Analyze content and return structured output."""
        ...


class OpenAIProvider(LLMProvider):
    """OpenAI implementation."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    async def generate(self, prompt, tools=None, **kwargs):
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            tools=tools,
            **kwargs,
        )
        return response.choices[0].message.content


class AnthropicProvider(LLMProvider):
    """Anthropic implementation."""
    ...


class LocalLLMProvider(LLMProvider):
    """Local LLM (Ollama, vLLM) implementation."""
    ...
```

---

## 6. Configuration

```python
# memharness with embedded agents
from memharness import MemoryHarness
from memharness.agents import AgentConfig
from memharness.llm import OpenAIProvider

memory = MemoryHarness(
    backend="postgresql://...",
    llm=OpenAIProvider(api_key="..."),  # Required for embedded agents
    agents=AgentConfig(
        enabled=True,  # Enable all embedded agents
        router={"enabled": True},
        entity_extraction={"enabled": True},
        summarization={
            "enabled": True,
            "policies": [
                {"condition": "age > 7d", "action": "summarize"},
            ],
        },
        consolidation={
            "enabled": True,
            "schedule": "0 3 * * *",
            "similarity_threshold": 0.9,
        },
        gc={
            "enabled": True,
            "schedule": "0 4 * * 0",
            "archive_after_days": 90,
        },
        tool_discovery={
            "enabled": True,
            "max_iterations": 10,
        },
        context_assembly={
            "enabled": True,
            "default_budget": 4000,
            "priorities": {
                "conversational": 0.4,
                "knowledge_base": 0.3,
                "entity": 0.15,
                "workflow": 0.10,
                "summary": 0.05,
            },
        },
        index_optimization={
            "enabled": True,
            "schedule": "0 5 * * 0",
        },
    ),
)

# Start agent scheduler
await memory.start_agents()
```

---

## 7. Monitoring & Observability

```python
class AgentMonitor:
    """Monitor embedded agent health and performance."""

    async def get_status(self) -> dict:
        return {
            "agents": {
                name: {
                    "status": agent.status,
                    "last_run": agent.last_run,
                    "runs_today": agent.runs_today,
                    "avg_duration_ms": agent.avg_duration_ms,
                    "errors_today": agent.errors_today,
                }
                for name, agent in self.agents.items()
            },
            "memory": {
                "total_memories": await self.memory.count(),
                "by_type": await self.memory.count_by_type(),
                "storage_used_mb": await self.memory.storage_used(),
            },
            "health": self._calculate_health(),
        }

    def _calculate_health(self) -> str:
        # Calculate overall health score
        ...
```

---

## 8. Benefits of AI-Native Memory Management

| Benefit | Description |
|---------|-------------|
| **Autonomous** | No manual memory maintenance required |
| **Intelligent** | AI understands content, context, relationships |
| **Consistent** | Deterministic policies ensure reliability |
| **Efficient** | Progressive loading, optimal context assembly |
| **Self-healing** | Auto-consolidation, GC, index optimization |
| **Observable** | Full monitoring and health reporting |
| **Pluggable** | Works with any LLM provider |

---

## 9. Comparison: Traditional vs AI-Native

| Aspect | Traditional Memory | AI-Native memharness |
|--------|-------------------|---------------------|
| **Routing** | Manual type specification | Auto-detected by Router Agent |
| **Deduplication** | Manual or rule-based | Semantic consolidation by AI |
| **Summarization** | Manual trigger | Policy-driven, automatic |
| **Entity extraction** | External pipeline | Built-in, on every write |
| **Context building** | Fixed templates | Intelligent assembly by AI |
| **Tool discovery** | Load all or fixed set | Progressive VFS discovery |
| **Maintenance** | Manual DBA work | Automated GC + Index agents |

---

*Design completed: 2026-03-22*
*This is the core differentiator for memharness*
