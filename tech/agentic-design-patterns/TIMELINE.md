# 📅 Agentic Design Patterns — Study Timeline
**Book:** Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems  
**Author:** Antonio Gulli | **Total Pages:** 424 | **Pre-Print:** [Amazon](https://www.amazon.com/Agentic-Design-Patterns-Hands-Intelligent/dp/3032014018/)  
**All Code Drive Folder:** [Google Drive](https://drive.google.com/drive/u/0/folders/1Y3U3IrYCiJ3E45Z8okR5eCg7OPnWQtPV)

---

## ⏱️ Total Estimated Time

| Section | Hours |
|---------|-------|
| Pre-reading (Preface, Intro, What is an Agent?) | 2h |
| Part 1 — Core Execution (Ch 1–7) | 14h |
| Part 2 — State & Memory (Ch 8–11) | 8h |
| Part 3 — Resilience & Retrieval (Ch 12–14) | 6h |
| Part 4 — Advanced Patterns (Ch 15–21) | 14h |
| Appendices A–G | 8h |
| **Total** | **~52 hours** |

---

## 📖 Chapter 0 — Preface, Introduction & What Makes an Agent?
**Folder:** `00_preface-and-introduction/` | **Pages:** 1–22 | **Estimated Time:** 2h

### Step-by-Step
1. Read Dedication, Acknowledgment, Foreword (30 min)
2. Read "A Thought Leader's Perspective: Power & Responsibility" by Goldman Sachs CIO (20 min)
3. Read Preface — what agentic systems are, why patterns matter, 3 frameworks used (30 min)
4. Read "What makes an AI system an Agent?" — 5-step loop, 4 levels of complexity, 5 future hypotheses (40 min)

### Topic Breakdown
| Topic | Description |
|-------|-------------|
| Agent Definition | Perceive → Plan → Act → Learn loop |
| 4 Levels of Agents | Level 0 (LLM only) → Level 3 (Multi-agent teams) |
| 5 Future Hypotheses | Generalist agent, personalization, embodiment, agent economy, metamorphic MAS |
| Frameworks Used | LangChain/LangGraph, CrewAI, Google ADK |

---

## 📖 Chapter 1 — Prompt Chaining
**Folder:** `01_prompt-chaining/` | **Pages:** 13 | **Estimated Time:** 2h  
**Code:** [Google Doc](https://docs.google.com/document/d/1u2y6tY48bw8nriDUuwWEf9s8g66vyIqBKSKZDOS-n0s/edit)

### Step-by-Step
1. Understand why single prompts fail for complex tasks (20 min)
2. Learn the pipeline pattern: output of step N → input of step N+1 (20 min)
3. Study structured output with JSON for reliable inter-step data (20 min)
4. Study Context Engineering vs Prompt Engineering distinction (20 min)
5. Run LangChain LCEL code example (two-step extraction + JSON transform) (40 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| Single Prompt Limitations | Instruction neglect, contextual drift, hallucination, context window overflow |
| Sequential Decomposition | Each step = focused prompt, output → next input |
| Structured Output | JSON/XML between steps = machine-readable, less ambiguity |
| Context Engineering | System prompt + RAG + tool outputs + history = full operational picture |
| LCEL Code | `prompt \| llm \| StrOutputParser()` piping |

---

## 📖 Chapter 2 — Routing
**Folder:** `02_routing/` | **Pages:** 14 | **Estimated Time:** 2h  
**Code:** [Google Doc](https://docs.google.com/document/d/18Q9kfZuCTL37ztrSjLxwf8Elr5UfAiAavmnj0IqSpbU/edit)

### Step-by-Step
1. Understand routing vs linear chains — conditional logic introduction (20 min)
2. Learn 4 routing types: LLM-based, embedding-based, rule-based, ML model-based (30 min)
3. Study LangChain `RunnableBranch` implementation (30 min)
4. Study Google ADK `sub_agents` auto-flow delegation (30 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| Routing Types | LLM-based, embedding similarity, rule/keyword, fine-tuned classifier |
| LangChain Routing | `RunnableBranch`, `coordinator_router_chain` |
| ADK Auto-Flow | `sub_agents=[]` triggers LLM-driven delegation |
| Use Cases | Customer support triage, coding assistant, document classification |

---

## 📖 Chapter 3 — Parallelization
**Folder:** `03_parallelization/` | **Pages:** 15 | **Estimated Time:** 2h  
**Code:** [Google Doc](https://docs.google.com/document/d/1PWhaXD_UNKgJaxYe3JBxRFRt3_B8Wm67CFxtSBQ4LkU/edit)

### Step-by-Step
1. Understand sequential vs parallel execution, when to use each (20 min)
2. Study `RunnableParallel` in LangChain LCEL (20 min)
3. Study ADK `ParallelAgent` + `SequentialAgent` with `output_key` for state passing (30 min)
4. Run parallel research agent (3 researchers → merger) code (50 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| When to Parallelize | Independent sub-tasks, API calls with latency, multi-API retrieval |
| LangChain Parallel | `RunnableParallel({...})`, `asyncio` for concurrency (not true parallelism — GIL) |
| ADK ParallelAgent | `sub_agents` run concurrently, `output_key` saves to session state |
| ADK SequentialAgent | Guaranteed order execution, `state["key"]` sharing between steps |

---

## 📖 Chapter 4 — Reflection
**Folder:** `04_reflection/` | **Pages:** 14 | **Estimated Time:** 2.5h  
**Code:** [Google Doc](https://docs.google.com/document/d/1K5jwqB6jh20uHL0TTWxqWOxFk-dzFxRvHzrRRV79hrg/edit)

### Step-by-Step
1. Understand self-correction loop: generate → evaluate → refine (20 min)
2. Learn Producer-Critic model (two-agent separation of concerns) (20 min)
3. Study LangChain reflection loop for code generation (iterative, max 5 rounds) (40 min)
4. Study ADK Generator + Reviewer sequential pipeline (30 min)
5. Understand trade-offs: quality vs latency/cost (10 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| Reflection Loop | Generate → Critique → Refine (repeat until `CODE_IS_PERFECT` or max iterations) |
| Producer-Critic | Separate agents = less cognitive bias in evaluation |
| Goal Setting Synergy | Reflection + Chapter 11 → corrective engine for deviations |
| Memory + Reflection | Conversation history enables cumulative learning across reflection cycles |
| Trade-offs | Higher quality but more tokens, latency, risk of context window overflow |

---

## 📖 Chapter 5 — Tool Use (Function Calling)
**Folder:** `05_tool-use/` | **Pages:** 21 | **Estimated Time:** 3h  
**Code:** [Google Doc](https://docs.google.com/document/d/1Nw6hRa7ItdLr_Tj5hF2q-OH8B_uPKb--RLn8SXZKA94/edit)

### Step-by-Step
1. Understand tool use flow: Tool Definition → LLM Decision → JSON call → Execution → Result (30 min)
2. Study `@langchain_tool` decorator + `create_tool_calling_agent` + `AgentExecutor` (40 min)
3. Study CrewAI `@tool` decorator + `Crew.kickoff()` (30 min)
4. Study ADK `google_search`, `BuiltInCodeExecutor`, `VSearchAgent` (40 min)
5. Understand "Tool Calling" vs "Function Calling" semantic distinction (10 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| Tool vs Function | Tool = broader (API, DB, agent, action); Function = specific Python call |
| LangChain Tool | `@langchain_tool`, `agent_scratchpad` placeholder, `AgentExecutor` |
| CrewAI Tool | `@tool("name")`, `Crew(tools=[...])`, returns raw data or raises `ValueError` |
| ADK Built-in Tools | `google_search`, `BuiltInCodeExecutor`, `VSearchAgent` (Vertex AI Search) |
| Vertex Extensions | Auto-executed by platform vs manual function calls |

---

## 📖 Chapter 6 — Planning
**Folder:** `06_planning/` | **Pages:** 13 | **Estimated Time:** 2h  
**Code:** [Google Doc](https://docs.google.com/document/d/1flxKGrbnF2g8yh3F-oVD5Xx7ZumId56HbFpIiPdkqLI/edit)

### Step-by-Step
1. Understand planning = dynamic how-discovery vs fixed workflows (20 min)
2. Study CrewAI `planner_writer_agent` with two-phase (plan → write) task (30 min)
3. Study Google DeepResearch agent: plan → search → reflect → report (30 min)
4. Study OpenAI Deep Research API: `o3-deep-research`, inline citations, intermediate steps (40 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| Planning vs Execution | Dynamic planning when "how" is unknown; fixed workflow when known |
| CrewAI Planning | Agent generates plan first, then follows it; `Process.sequential` |
| Google DeepResearch | Agentic pipeline: iterative search → gap analysis → synthesis with citations |
| OpenAI Deep Research API | `o3-deep-research-2025-06-26`, `web_search_preview` tool, `annotations` for citations |
| Adaptability | Initial plan = starting point; agent re-plans on obstacles |

---

## 📖 Chapter 7 — Multi-Agent Collaboration
**Folder:** `07_multi-agent/` | **Pages:** 19 | **Estimated Time:** 3h  
**Code:** [Colab Notebook](https://colab.research.google.com/drive/15XCzDOvBhIQaZ__xkvruf5sP9OznAbK9)

### Step-by-Step
1. Understand 6 collaboration models (Single → Network → Supervisor → Hierarchical → Custom) (30 min)
2. Study CrewAI researcher + writer pipeline with `context=[research_task]` (30 min)
3. Study ADK hierarchical agents: coordinator → `[greeter, task_doer]` (30 min)
4. Study ADK LoopAgent with condition checker + `EventActions(escalate=True)` (30 min)
5. Study ADK SequentialAgent + ParallelAgent + Agent-as-Tool patterns (40 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| 6 MAS Architectures | Single, Network (P2P), Supervisor (central hub), Supervisor-as-Tool, Hierarchical, Custom |
| CrewAI Crew | `agents`, `tasks`, `Process.sequential`, `context=[prior_task]` for chaining |
| ADK Parent-Child | `sub_agents=[]` sets `parent_agent` reference automatically |
| ADK LoopAgent | `max_iterations`, `EventActions(escalate=True)` to break loop |
| Agent-as-Tool | `agent_tool.AgentTool(agent=...)` wraps agent as callable tool for another agent |

---

## 📖 Chapter 8 — Memory Management
**Folder:** `08_memory-management/` | **Pages:** 22 | **Estimated Time:** 3h  
**Code:** [Google Doc](https://docs.google.com/document/d/1ux_n8n3T4bYndOjs1DKW5ccpC802KISdy2IWnlvYbas/edit)

### Step-by-Step
1. Understand Short-term (context window) vs Long-term (external storage) memory (20 min)
2. Study ADK Session, State, MemoryService triad (30 min)
3. Study `output_key` pattern vs `EventActions.state_delta` for state updates (30 min)
4. Study `InMemorySessionService` vs `DatabaseSessionService` vs `VertexAiSessionService` (20 min)
5. Study LangChain `ChatMessageHistory`, `ConversationBufferMemory`, `InMemoryStore` (40 min)
6. Study Vertex Memory Bank (`VertexAiMemoryBankService`) (20 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| ADK Session | Conversation thread with `id`, `events`, `state`, `last_update_time` |
| State Prefixes | No prefix = session-scoped, `user:` = cross-session, `app:` = global, `temp:` = current turn only |
| Memory vs State | State = scratchpad for current session; Memory = searchable long-term across sessions |
| LangChain Memory | `ConversationBufferMemory(memory_key="history", return_messages=True)` for chat models |
| LangGraph Store | `store.put(namespace, key, data)` / `store.search(namespace, query=...)` |
| 3 Long-term Types | Semantic (facts), Episodic (experiences/few-shot examples), Procedural (instructions/prompts) |

---

## 📖 Chapter 9 — Learning and Adaptation
**Folder:** `09_learning-and-adaptation/` | **Pages:** 13 | **Estimated Time:** 2h  
**Code:** [Google Doc](https://docs.google.com/document/d/1XVMp4RcRkoUJTVbrP2foWZX703CUJpWkrhyFU2cfUOA/edit)

### Step-by-Step
1. Survey 6 learning types: RL, Supervised, Unsupervised, Few/Zero-shot, Online, Memory-based (20 min)
2. Understand PPO vs DPO for LLM alignment (20 min)
3. Study SICA (Self-Improving Coding Agent) — meta-improvement loop (30 min)
4. Study AlphaEvolve + OpenEvolve for evolutionary algorithm optimization (30 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| PPO | Reinforcement learning with "clipping" for safe policy updates |
| DPO | Direct preference optimization — skips reward model, trains directly on preferences |
| SICA | Agent edits its own code → benchmarks → selects best → repeats; Docker sandboxed |
| AlphaEvolve | Gemini Flash (generate) + Pro (refine) + evaluator → evolutionary improvement |
| OpenEvolve | Open-source; Controller → LLM Ensemble → Evaluator Pool → Program Database |

---

## 📖 Chapter 10 — Model Context Protocol (MCP)
**Folder:** `10_model-context-protocol/` | **Pages:** 16 | **Estimated Time:** 2.5h  
**Code:** [Google Doc](https://docs.google.com/document/d/1HXXJOQIMWowtLw4WMiSR360caDAlZPtl5dPPgvq9IT4/edit)

### Step-by-Step
1. Understand MCP vs Function Calling — standardization vs proprietary (20 min)
2. Study MCP client-server architecture: LLM → Client → Server → 3P Service (20 min)
3. Study ADK `MCPToolset` with `StdioServerParameters` (filesystem server) (40 min)
4. Study FastMCP server creation with `@mcp_server.tool` decorator (30 min)
5. Study FastMCP client consumption via `HttpServerParameters` in ADK (20 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| MCP vs Function Calling | MCP = open standard, dynamic discovery, reusable; FC = proprietary, static |
| Transport | Local: JSON-RPC over STDIO; Remote: Streamable HTTP + SSE |
| ADK MCPToolset | `StdioServerParameters(command='npx', args=[...])` or `HttpServerParameters(url=...)` |
| FastMCP | `@mcp_server.tool` → auto schema from type hints + docstring; `mcp_server.run(transport="http")` |
| Caveats | MCP doesn't guarantee agent-friendly data format; must design APIs for agents |

---

## 📖 Chapter 11 — Goal Setting and Monitoring
**Folder:** `11_goal-setting-and-monitoring/` | **Pages:** 13 | **Estimated Time:** 2h  
**Code:** [Google Doc](https://docs.google.com/document/d/1bE4iMljhppqGY1p48gQWtZvk6MfRuJRCiba1yRykGNE/edit)

### Step-by-Step
1. Understand Goal Setting pattern: SMART goals + monitoring = reactive → proactive agent (20 min)
2. Study code agent example: task → generate → critique → `goals_met(True/False)` loop (40 min)
3. Understand caveats: LLM may misinterpret goals, same LLM judging own work (20 min)
4. Explore multi-agent crew approach for better separation (20 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| SMART Goals | Specific, Measurable, Achievable, Relevant, Time-bound |
| Generate-Critique Loop | `generate_response()` → `get_code_feedback()` → `goals_met()` returns True/False |
| LLM-as-Judge | Ask LLM to judge if goals met; output must be parseable ("True" or "False") |
| Multi-Agent QA | Peer Programmer → Code Reviewer → Test Writer → Documenter → Prompt Refiner |

---

## 📖 Chapter 12 — Exception Handling and Recovery
**Folder:** `12_exception-handling-and-recovery/` | **Pages:** 8 | **Estimated Time:** 1.5h  
**Code:** [Google Doc](https://docs.google.com/document/d/18vvNESEwHnVUREzIipuaDNCnNAREGqEfy9MQYC9wb4o/edit)

### Step-by-Step
1. Study the 3-stage framework: Error Detection → Error Handling → Recovery (20 min)
2. Study ADK SequentialAgent fallback pattern: primary_handler → fallback_handler → response_agent (40 min)
3. Understand state-based fallback: `state["primary_location_failed"]` flag (20 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| Error Detection | Invalid tool output, API 404/500, timeouts, nonsensical responses |
| Error Handling | Logging, retries, fallbacks, graceful degradation, notifications |
| Recovery | State rollback, self-correction, re-planning, escalation to human |
| ADK Pattern | `primary_handler` → sets `state["failed"]` → `fallback_handler` checks flag → `response_agent` |

---

## 📖 Chapter 13 — Human-in-the-Loop
**Folder:** `13_human-in-the-loop/` | **Pages:** 9 | **Estimated Time:** 1.5h  
**Code:** [Google Doc](https://docs.google.com/document/d/1RZ5-2fykDQKOBx01pwfKkDe0GCs5ydca7xW9Q4wqS_M/edit)

### Step-by-Step
1. Understand HITL pattern components: oversight, intervention, feedback, decision augmentation (20 min)
2. Study personalization callback injecting customer data into LLM prompt before each call (30 min)
3. Study `escalate_to_human` tool in ADK technical support agent (20 min)
4. Understand "Human-on-the-loop" variant (policy-setting vs direct oversight) (10 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| 6 HITL Aspects | Oversight, Intervention, Feedback for Learning, Decision Augmentation, Collaboration, Escalation Policies |
| ADK Callback | `before_model_callback` injects personalization data from `session.state` |
| Escalation | `escalate_to_human(issue_type)` as a tool the LLM can call autonomously |
| Caveats | Not scalable for millions of tasks; requires domain expert operators; privacy concerns |
| Human-on-loop | AI handles immediate actions; human sets overarching policy |

---

## 📖 Chapter 14 — Knowledge Retrieval (RAG)
**Folder:** `14_knowledge-retrieval-rag/` | **Pages:** 18 | **Estimated Time:** 3h  
**Code:** [Google Doc](https://docs.google.com/document/d/1asVTObtzIye0I9ypAztaeeI_sr_Hx2TORE02uUuqH_c/edit)

### Step-by-Step
1. Understand embeddings, text similarity, semantic distance, vector databases (30 min)
2. Study chunking strategies + retrieval: vector search, BM25, hybrid search (20 min)
3. Study Graph RAG vs standard RAG tradeoffs (20 min)
4. Study Agentic RAG: 4 agent capabilities (validation, conflict reconciliation, multi-step, tool use) (20 min)
5. Run ADK Google Search RAG + LangChain/Weaviate RAG pipeline code (50 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| Embeddings | High-dim vectors; similar meaning = close vectors; HNSW for fast lookup |
| Vector DBs | Pinecone, Weaviate, Chroma, Milvus, Qdrant; pgvector for Postgres |
| Graph RAG | Knowledge graph instead of vector DB; handles multi-document synthesis; higher complexity |
| Agentic RAG | Agent validates sources, reconciles conflicts, decomposes questions, uses external tools |
| Vertex AI RAG | `VertexAiRagMemoryService(rag_corpus=..., similarity_top_k=5)` |
| LangGraph RAG | `StateGraph` with `retrieve` → `generate` nodes; `Weaviate.from_documents()` |

---

## 📖 Chapter 15 — Inter-Agent Communication (A2A)
**Folder:** `15_inter-agent-communication-a2a/` | **Pages:** 15 | **Estimated Time:** 2.5h  
**Code:** [Google Doc](https://docs.google.com/document/d/1UHTEDCmSM1nwB-iyMoHuYzVcu_B_4KkJ2ITGGUKqo8s/edit)

### Step-by-Step
1. Study A2A core concepts: Core Actors, Agent Card, Agent Discovery, Tasks, Security (30 min)
2. Understand A2A vs MCP: A2A = agent-to-agent coordination; MCP = agent-to-tool (20 min)
3. Study Agent Card JSON structure with skills, capabilities, authentication (20 min)
4. Study 4 interaction mechanisms: sync, async polling, SSE streaming, webhooks (20 min)
5. Study ADK + A2A Calendar Agent code (A2AStarletteApplication) (40 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| A2A Actors | User → Client Agent → Server Agent (opaque) |
| Agent Card | JSON with name, url, version, skills, capabilities, authentication |
| Discovery | Well-Known URI (`/.well-known/agent.json`), Curated Registry, Direct Config |
| Interaction | Sync `sendTask`, Streaming `sendTaskSubscribe`, async polling, webhooks |
| ADK A2A | `ADKAgentExecutor`, `A2AStarletteApplication`, `InMemoryTaskStore`, Uvicorn |
| A2A Supporters | Atlassian, Box, LangChain, MongoDB, Salesforce, SAP, ServiceNow, Microsoft |

---

## 📖 Chapter 16 — Resource-Aware Optimization
**Folder:** `16_resource-aware-optimization/` | **Pages:** 16 | **Estimated Time:** 2.5h  
**Code:** [Google Doc](https://docs.google.com/document/d/1e6XimYczKmhX9zpqEyxLFWPQgGuG0brp7Hic2sFl_qw/edit)

### Step-by-Step
1. Understand resource optimization: cost, latency, energy tradeoffs (20 min)
2. Study Router Agent pattern: classify → route to Flash (simple) or Pro (complex) (30 min)
3. Study OpenAI prompt classification code (simple/reasoning/internet_search routing) (40 min)
4. Study OpenRouter automated model selection + sequential fallback (20 min)
5. Survey 8 additional optimization techniques (contextual pruning, energy efficiency, etc.) (20 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| Dynamic Model Switching | Flash for simple, Pro for complex; query length or LLM-based classification |
| Router Agent | Classify → `assign_to_flash_agent()` or `assign_to_pro_agent()` |
| Critique Agent | Evaluates responses, flags poor routing, feeds back to improve router |
| OpenRouter | `"model": "openrouter/auto"` or `"models": ["primary", "fallback"]` |
| 8 Techniques | Adaptive tool selection, context pruning, resource prediction, cost-sensitive exploration, energy efficiency, parallelization awareness, learned allocation, graceful degradation |

---

## 📖 Chapter 17 — Reasoning Techniques
**Folder:** `17_reasoning-techniques/` | **Pages:** 24 | **Estimated Time:** 3.5h  
**Code:** [Google Doc](https://docs.google.com/document/d/10ndlCB39BWjyFRWKpcoKib4vuPD1ojD-x0-ynMaf5uw/edit)

### Step-by-Step
1. Study CoT (Chain-of-Thought): zero-shot "think step by step" vs few-shot CoT (30 min)
2. Study Tree-of-Thought: explore multiple branches, backtrack, evaluate (20 min)
3. Study Self-Correction / Self-Refinement with PAL (code execution) (20 min)
4. Study RLVR (Reinforcement Learning with Verifiable Rewards) for reasoning models (20 min)
5. Study ReAct loop: Thought → Action → Observation (repeat) (20 min)
6. Study CoD (Chain of Debates) + GoD (Graph of Debates) (20 min)
7. Study MASS framework for automated MAS optimization (30 min)
8. Study Scaling Inference Law + Deep Research pattern (30 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| CoT | "Let's think step by step" → explicit reasoning chain; temperature=0 for deterministic answers |
| Tree-of-Thought | Multiple simultaneous reasoning branches; backtracking; self-evaluation |
| PAL | LLM generates Python code → execute for precise calculations; hybrid text+code |
| RLVR | Train on verifiable problems (math, code); model learns via trial-and-error; produces long CoT |
| ReAct | `Thought: ...` → `Action: search(query)` → `Observation: result` → repeat |
| CoD/GoD | Multi-model debate for accuracy/bias reduction; graph structure for non-linear reasoning |
| MASS | Block-level prompt optimization → topology search → workflow-level joint optimization |
| Scaling Inference Law | More "thinking time" at inference → better quality; smaller model + inference budget ≈ larger model |

---

## 📖 Chapter 18 — Guardrails / Safety Patterns
**Folder:** `18_guardrails-safety-patterns/` | **Pages:** 20 | **Estimated Time:** 3h  
**Code:** [Google Doc](https://docs.google.com/document/d/1C07AuMur6-infwE0viCp4QtAy_wWI-uceFm6MaYHQGk/edit)

### Step-by-Step
1. Understand 6 guardrail implementation points (input, output, prompt, tool, external, HITL) (20 min)
2. Study CrewAI content policy enforcer with Pydantic `PolicyEvaluation` schema + `guardrail=` task param (50 min)
3. Study ADK `before_tool_callback` for parameter validation (30 min)
4. Study LLM-based safety guardrail prompt (jailbreak detection, hate speech, off-topic) (30 min)
5. Study "Engineering Reliable Agents" principles (modularity, observability, least privilege) (20 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| 6 Guardrail Layers | Input validation, output filtering, prompt constraints, tool restrictions, external moderation, HITL |
| CrewAI Guardrail | `Task(guardrail=validate_fn, output_pydantic=PolicyEvaluation)` → auto-retry on validation failure |
| ADK Callback | `before_tool_callback(tool, args, tool_context)` → return dict to block, None to allow |
| Safety Prompt | Classifies: jailbreaking, prohibited content, off-topic, brand disparagement → `{"decision": "safe"\|"unsafe"}` |
| Engineering Principles | Modularity/separation of concerns, structured logging, principle of least privilege |

---

## 📖 Chapter 19 — Evaluation and Monitoring
**Folder:** `19_evaluation-and-monitoring/` | **Pages:** 19 | **Estimated Time:** 3h  
**Code:** [Google Doc](https://docs.google.com/document/d/1ImOZcw6yeb7a-uRBMNP1VdovYfyip4IdsAcLu9yue-0/edit)

### Step-by-Step
1. Study 3 evaluation methods: human, LLM-as-judge, automated metrics (30 min)
2. Study agent trajectory evaluation: exact match, in-order, any-order, precision, recall (30 min)
3. Study `LLMJudgeForLegalSurvey` class with structured rubric + JSON output (40 min)
4. Study ADK eval methods: web UI, pytest `AgentEvaluator.evaluate()`, `adk eval` CLI (30 min)
5. Study "Contractor Model" — formalized contract → negotiation → iterative execution → subcontracts (30 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| Eval Methods | Human (accurate, slow), LLM-as-Judge (scalable, limited), Automated (fast, narrow) |
| Trajectory Eval | Expected tool sequence vs actual; exact/in-order/any-order matching |
| LLM-as-Judge | Rubric with criteria (1-5 scores); structured JSON output; `response_mime_type="application/json"` |
| ADK Eval Formats | Test files (single session, unit tests), evalset files (multi-session, integration tests) |
| Contractor Model | Formal contract spec → agent negotiates → self-validates → subcontracts for hierarchy |

---

## 📖 Chapter 20 — Prioritization
**Folder:** `20_prioritization/` | **Pages:** 10 | **Estimated Time:** 1.5h  
**Code:** [Google Doc](https://docs.google.com/document/d/1v96Oobio6xDOqbK8ejsXjmOc4Dp2uoLMo5_gfJgi-NE/edit)

### Step-by-Step
1. Understand 6 prioritization criteria: urgency, importance, dependencies, resources, cost/benefit, preferences (20 min)
2. Study LangChain Project Manager Agent: create → prioritize → assign → list (50 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| Prioritization Levels | High-level goal selection, sub-task ordering, immediate action selection |
| Criteria | Urgency (P0/P1/P2), importance, dependencies, resource availability, cost/benefit |
| PM Agent Code | `SuperSimpleTaskManager` + 4 tools + `create_react_agent` + `ConversationBufferMemory` |
| Dynamic Re-prioritization | Agent adjusts focus in real-time as new critical events emerge |

---

## 📖 Chapter 21 — Exploration and Discovery
**Folder:** `21_exploration-and-discovery/` | **Pages:** 14 | **Estimated Time:** 2h  
**Code:** [Google Doc](https://docs.google.com/document/d/1H6HmUYcy5kugt5gt7Kh2Zzb8C62d5pu36RsgMNDCX24/edit)

### Step-by-Step
1. Study Google Co-Scientist architecture: 6 specialized agents (Generation, Reflection, Ranking, Evolution, Proximity, Meta-Review) (30 min)
2. Study Agent Laboratory framework: Literature Review → Experimentation → Report Writing (30 min)
3. Study tripartite ReviewersAgent with 3 different critic personas (20 min)
4. Study Professor + PostDoc + ML Engineer + SW Engineer agent hierarchy (30 min)

### Topic Breakdown
| Topic | Key Concepts |
|-------|-------------|
| Co-Scientist | Gemini Flash (generate) + Pro (refine); Elo-based tournament ranking; test-time compute scaling |
| Co-Scientist Results | 78.4% GPQA diamond accuracy; independent rediscovery of decade-long research in 2 days |
| Agent Laboratory | `ReviewersAgent` with 3 critic types; `ProfessorAgent` + `PostdocAgent` + ML/SW engineer roles |
| Tripartite Judgment | 3 reviewers (insights, impact, novelty) → collective scoring → mimic peer review |

---

## 📚 Appendices

### Appendix A — Advanced Prompting Techniques
**Folder:** `appendix-a_advanced-prompting/` | **Pages:** 29 | **Estimated Time:** 3h

| Topic | Key Concepts |
|-------|-------------|
| Core Principles | Clarity, conciseness, action verbs, positive instructions, iteration |
| Prompting Types | Zero-shot, One-shot, Few-shot, Many-shot (for long context models) |
| Structuring | System prompting, role prompting, delimiters, context engineering, structured output |
| Reasoning | CoT (zero/few-shot), Self-Consistency, Step-Back, Tree-of-Thoughts |
| Action | Tool use/function calling, ReAct (Thought→Action→Observation loop) |
| Advanced | APE (Automatic Prompt Engineering), DSPy programmatic optimization, iterative refinement |
| Special | Code prompting, multimodal prompting, Pydantic for structured output, Google Gems |

### Appendix B — AI Agentic Interactions: From GUI to Real World
**Folder:** `appendix-b_gui-to-real-world/` | **Pages:** 7 | **Estimated Time:** 1h

| Tool | Description |
|------|-------------|
| ChatGPT Operator | Desktop GUI automation across applications |
| Google Project Mariner | Chrome-based web agent |
| Anthropic Computer Use | Desktop screenshot + mouse/keyboard control |
| Browser Use | Open-source DOM-based browser automation library |
| Google Project Astra | Multimodal real-world agent (camera + microphone) |
| Gemini Live | Real-time voice conversation with interruption support |
| Vibe Coding | Conversational, iterative AI-assisted development |

### Appendix C — Quick Overview of Agentic Frameworks
**Folder:** `appendix-c_agentic-frameworks/` | **Pages:** 8 | **Estimated Time:** 1h

| Framework | Best For |
|-----------|----------|
| LangChain (LCEL) | Linear DAG workflows, simple chains |
| LangGraph | Stateful cyclical graphs, complex reasoning loops |
| Google ADK | Production multi-agent systems, Google Cloud integration |
| CrewAI | Role-based team simulation, collaborative agents |
| Microsoft AutoGen | Conversation-driven multi-agent interactions |
| LlamaIndex | Data-intensive RAG applications |
| Haystack | Enterprise-scale search systems |
| MetaGPT | SOP-driven software development simulation |
| Strands Agents (AWS) | Lightweight, model-agnostic, MCP-native |

### Appendix D — Building an Agent with AgentSpace
**Folder:** `appendix-d_agentspace/` | **Pages:** 6 | **Estimated Time:** 30 min

### Appendix E — AI Agents on the CLI
**Folder:** `appendix-e_ai-agents-on-cli/` | **Pages:** 5 | **Estimated Time:** 1h

| Tool | Strength |
|------|----------|
| Claude CLI (Claude Code) | Architecture-level refactoring, pair programming |
| Gemini CLI | Multimodal, open-source, Google Cloud integration |
| Aider | Git-centric TDD, automatic commits, model-agnostic |
| GitHub Copilot CLI | GitHub ecosystem, issue-to-PR automation |

### Appendix G — Coding Agents
**Folder:** `appendix-g_coding-agents/` | **Pages:** 17 | **Estimated Time:** 1h

Human-led framework with 5 specialist agents:
- **Scaffolder** — writes new code/features
- **Test Engineer** — writes comprehensive test suites
- **Documenter** — generates API docs and READMEs  
- **Optimizer** — proposes refactoring + performance improvements
- **Process Agent (Supervisor)** — critique → reflection → prioritized feedback

---

## 🗺️ Learning Path by Goal

### If you want to build a simple LLM pipeline:
Ch 1 (Chaining) → Ch 2 (Routing) → Appendix A (Prompting)

### If you want to build a production agent:
Ch 5 (Tools) → Ch 6 (Planning) → Ch 8 (Memory) → Ch 18 (Guardrails) → Ch 19 (Evaluation)

### If you want multi-agent systems:
Ch 7 (Multi-Agent) → Ch 15 (A2A) → Ch 10 (MCP) → Ch 16 (Resource Optimization)

### If you want cutting-edge reasoning:
Ch 17 (Reasoning) → Ch 4 (Reflection) → Ch 21 (Exploration)

### If you want safety + reliability:
Ch 18 (Guardrails) → Ch 12 (Exception Handling) → Ch 13 (HITL) → Ch 19 (Evaluation)

---

*Generated from: Agentic Design Patterns by Antonio Gulli (2025)*
