# LangChain Middleware Integration Strategy

## Date: 2026-03-23 (updated)

## Key Insight
LangChain's `create_agent` + middleware system is the RIGHT abstraction.
memharness should NOT reimplement agents. Instead:

### What we provide:
1. **Memory Tools** (BaseTool) → plug into any `create_agent` ✅ done
2. **Memory Middleware** → inject memory context before/after model calls
3. **MemharnessChatHistory** → agent persistence ✅ done
4. **Embeddings** → via langchain-huggingface ✅ done

### Memory Middleware Design

```python
from langchain.agents.middleware import before_model, after_model, AgentState

@before_model
def inject_memory_context(state: AgentState, runtime: Runtime):
    """Inject relevant memories into the conversation before each model call."""
    harness = runtime.config["memharness"]
    query = state["messages"][-1].content
    context = await harness.assemble_context(query, thread_id=...)
    # Prepend context as system message
    return {"messages": [SystemMessage(content=context)] + state["messages"]}

@after_model  
def store_interaction(state: AgentState, runtime: Runtime):
    """Store the model's response in memory after each call."""
    harness = runtime.config["memharness"]
    last_msg = state["messages"][-1]
    await harness.add_conversational(thread_id=..., role="assistant", content=last_msg.content)
```

### Usage Pattern
```python
from memharness import MemoryHarness
from memharness.middleware import MemoryContextMiddleware
from langchain.agents import create_agent

harness = MemoryHarness("sqlite:///memory.db")
await harness.connect()

agent = create_agent(
    model="anthropic:claude-sonnet-4-6",
    tools=[...],  # user's tools + memharness memory tools
    middleware=[
        MemoryContextMiddleware(harness=harness, thread_id="conv-1"),
        SummarizationMiddleware(model="gpt-4.1-mini"),
    ],
)
```

### Built-in Middleware We Can Leverage (don't reimplement):
- SummarizationMiddleware → replaces our SummarizerAgent
- Filesystem middleware → complementary to our memory storage
- Tool retry → for reliable memory operations
- Model fallback → for agent resilience

### What Our Custom Middleware Adds:
- MemoryContextMiddleware → inject relevant memories before model calls
- EntityExtractionMiddleware → extract entities after model calls
- MemoryPersistenceMiddleware → auto-save conversations
