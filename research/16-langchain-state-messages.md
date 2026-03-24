# LangChain Agent State + memharness Integration Pattern

## Date: 2026-03-23

## How LangChain Agents Store Messages

LangChain's `create_agent` builds a LangGraph graph. The agent state has a `messages` key:

```python
# Agent state (internal)
state = {
    "messages": [
        HumanMessage(content="What's the weather?"),
        AIMessage(content="Let me check...", tool_calls=[...]),
        ToolMessage(content="72°F, sunny"),
        AIMessage(content="It's 72°F and sunny!"),
    ]
}
```

The `messages` list grows with every turn. This is the conversation memory.

## Integration Pattern: Middleware on state["messages"]

The cleanest integration is a middleware that:
1. **BEFORE model**: loads past messages from memharness → prepends to state["messages"]
2. **AFTER model**: saves new messages from state["messages"] → writes to memharness

```python
from langchain.agents.middleware import AgentMiddleware
from memharness import MemoryHarness

class MemharnessConversationMiddleware(AgentMiddleware):
    def __init__(self, harness: MemoryHarness, thread_id: str):
        super().__init__()
        self.harness = harness
        self.thread_id = thread_id
        self._saved_count = 0

    async def abefore_model(self, state, runtime):
        # Load past conversation from memharness
        memories = await self.harness.get_conversational(self.thread_id, limit=20)
        if not memories:
            return None
        # Convert to LangChain messages and prepend
        from langchain_core.messages import HumanMessage, AIMessage
        past_messages = []
        for m in memories:
            role = m.metadata.get("role", "user")
            if role in ("user", "human"):
                past_messages.append(HumanMessage(content=m.content))
            elif role in ("assistant", "ai"):
                past_messages.append(AIMessage(content=m.content))
        # Inject past messages before current messages
        current = state.get("messages", [])
        return {"messages": past_messages + list(current)}

    async def aafter_model(self, state, runtime):
        # Save new messages to memharness
        messages = state.get("messages", [])
        new_messages = messages[self._saved_count:]
        for msg in new_messages:
            role = "user" if isinstance(msg, HumanMessage) else "assistant"
            await self.harness.add_conversational(self.thread_id, role, msg.content)
        self._saved_count = len(messages)
        return None
```

## Key Insight
- The TOOLS (12 of them) give the agent self-awareness INSIDE the loop
- The MIDDLEWARE gives the agent persistent memory ACROSS sessions
- memharness package provides the tools (in package)
- The middleware pattern is for the DEV to implement (in docs as example)

## Rest of memory types (KB, entity, workflow, etc.)
These are accessed via the 12 tools INSIDE the loop. The agent decides when to search/write.
Only conversation history needs the middleware because it's the PRIMARY state.
