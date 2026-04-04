# 🃏 AsyncIO Flashcards

> From: `python/asyncio/`
> Last updated: 2026-03-21

---

### ⚡ Core Concepts

<details>
<summary>❓ AsyncIO ka matlab kya hai? Kya yeh code ko faster banata hai?</summary>

AsyncIO = Python's built-in library for **concurrent** code. It does NOT make code faster — it lets you **do other work while waiting** for IO (network, DB, files) instead of sitting idle.

> Subway vs McDonald's — McDonald's takes next order while your food is cooking. Not faster cooking, just less idle time!
</details>

<details>
<summary>❓ Event Loop kya hai?</summary>

The **engine** that runs all async code. It's a scheduler — tracks tasks, runs them when ready, suspends when waiting.

`asyncio.run(main())` → starts loop → runs tasks → closes when done.

Without event loop = no async code works. Orchestra ka conductor!
</details>

<details>
<summary>❓ 3 types of Awaitables?</summary>

1. **Coroutines** — created by calling `async def` functions. Pausable functions.
2. **Tasks** — wrappers around coroutines, scheduled on event loop independently.
3. **Futures** — low-level promise objects. Rarely used directly.

You can only `await` awaitables, and only inside `async` functions.
</details>

<details>
<summary>❓ Coroutine Function vs Coroutine Object?</summary>

**Function:** `async def fetch_data():` — the definition.
**Object:** `coro = fetch_data()` — the awaitable returned when you CALL it.

Calling an async function does NOT run it! Just creates the object. Must `await` or `create_task` to run.
</details>

<details>
<summary>❓ create_task vs bare await — kya farak?</summary>

`await fetch_data(1)` → schedules AND runs to completion. One at a time. **No concurrency.**

`asyncio.create_task(fetch_data(1))` → schedules immediately on event loop. Can run alongside other tasks. **Concurrency!**

This is the #1 mistake beginners make.
</details>

<details>
<summary>❓ await ka actual meaning kya hai?</summary>

`await` = "**Don't move past this line until this thing is done.**"

It does NOT mean "run this now." The event loop decides order. `await` just guarantees you won't proceed until the result is ready.
</details>

<details>
<summary>❓ time.sleep vs asyncio.sleep?</summary>

`time.sleep(2)` → **Blocks entire event loop.** No other task runs. Highway pe road block.

`asyncio.sleep(2)` → Suspends only current coroutine. Event loop runs other tasks. Rest stop — others drive past.
</details>

---

### 🛠️ Patterns & Tools

<details>
<summary>❓ Blocking sync code async mein kaise chalayein?</summary>

**IO-bound sync code → Threads:**
```python
asyncio.to_thread(sync_function, arg1, arg2)
```

**CPU-bound sync code → Processes:**
```python
loop.run_in_executor(ProcessPoolExecutor(), func, arg)
```

Both wrap sync code in a future the event loop can manage.
</details>

<details>
<summary>❓ gather vs TaskGroup?</summary>

| | gather (return_exceptions=True) | TaskGroup |
|--|---|---|
| One fails | Others keep running | All cancel |
| Results | Mix of results + exceptions | All succeed or ExceptionGroup |
| Use when | Some failures OK (URL crawling) | All-or-nothing (transactions) |

Never use gather with default `return_exceptions=False`!
</details>

<details>
<summary>❓ Semaphore kya karta hai?</summary>

Limits max concurrent operations. Don't blast 1000 requests at once!

```python
sem = asyncio.Semaphore(4)  # Max 4 at a time
async with sem:
    await download(url)
```
</details>

<details>
<summary>❓ IO-bound vs CPU-bound kaise pehchanein?</summary>

**IO-bound:** Waiting on external stuff. Keywords: fetch, get, request, download, query. → **AsyncIO or Threads**

**CPU-bound:** Heavy computation. Keywords: compute, calculate, process, transform. → **Processes**

Not sure? Profile with **Scalene** — shows Python time (CPU) vs system time (IO).
</details>

---

### ⚠️ Common Pitfalls

<details>
<summary>❓ 4 most common AsyncIO mistakes?</summary>

1. **Forgot to await** → task silently cancelled, no error
2. **Script ends before tasks finish** → incomplete results
3. **Blocking code inside async** (time.sleep, requests.get) → kills concurrency
4. **Too many concurrent requests** → overwhelms machine + servers → use Semaphore
</details>

---

> 💡 *Bolke batao — padhke nahi, bolke yaad hota hai!* 🗣️
