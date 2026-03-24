# 🃏 Threading Flashcards

> From: threading/ + related: asyncio/
> Last updated: 2026-03-24

---

### 📌 Core Threading

<details>
<summary>❓ What's the difference between concurrency and parallelism?</summary>

**Concurrency** (threading) = one CPU, tasks overlap during I/O waits. Like one person switching between tasks.
**Parallelism** (multiprocessing) = multiple CPUs, tasks truly run at the same time. Like multiple people each doing a task.

> Concurrency = ek chef, multiple burners. Parallelism = multiple chefs! 👨‍🍳
</details>

<details>
<summary>❓ When should you use threading vs multiprocessing?</summary>

| Task Type | Use |
|-----------|-----|
| **I/O-bound** (network, disk, sleep) | 🧵 Threading |
| **CPU-bound** (computation, image processing) | ⚙️ Multiprocessing |

⚠️ Threading on CPU-bound tasks can be **slower** due to thread overhead + GIL.
</details>

<details>
<summary>❓ What's the GIL and why does it matter for threading?</summary>

**GIL (Global Interpreter Lock)** = Python only lets one thread execute bytecode at a time. This means threads can't truly run Python code in parallel. They can only overlap during I/O waits (when the GIL is released). For CPU-bound work, use multiprocessing to bypass the GIL.
</details>

<details>
<summary>❓ Why must you NOT put parentheses on the target function?</summary>

`Thread(target=do_something)` ✅ — passes the function object (thread will call it)
`Thread(target=do_something())` ❌ — **executes immediately** and passes the return value (None)

Same trap as `button.onClick = handler` vs `handler()` in JS!
</details>

<details>
<summary>❓ Why can't you `.join()` inside the thread creation loop?</summary>

`.join()` blocks until that thread finishes. Inside the loop: start thread 1 → wait for it to finish → start thread 2 → wait... = **sequential execution**. You must start ALL threads first, then join ALL of them in a second loop.
</details>

<details>
<summary>❓ What does ThreadPoolExecutor give you over manual threads?</summary>

- Cleaner code (fewer lines)
- Context manager auto-joins all threads at exit
- `submit()` returns Future objects (check status, get results)
- `map()` for running function over iterable
- Easy to switch to `ProcessPoolExecutor` for multiprocessing
</details>

<details>
<summary>❓ submit + as_completed vs map — when to use which?</summary>

| | `submit()` + `as_completed()` | `map()` |
|--|-------------------------------|---------|
| **Result order** | ⚡ Completion order | 📋 Start order |
| **Returns** | Future objects | Results directly |
| **Use when** | You want fastest results first | Order matters |

> `as_completed` = race (pehle aaya, pehle result). `map` = roll number order! 🏁
</details>

<details>
<summary>❓ What happens to exceptions in ThreadPoolExecutor?</summary>

With `submit()`: exception raised when you call `.result()` on the Future.
With `map()`: exception raised when you iterate over results.
In neither case does the exception raise during thread execution itself.
</details>

---

### 🔗 From: AsyncIO (Cross-Topic)

<details>
<summary>❓ Threading vs AsyncIO — both do I/O concurrency. When to pick which?</summary>

| | Threading | AsyncIO |
|--|-----------|---------|
| **When** | Existing sync code, simple parallelism | New code, high concurrency (1000s of connections) |
| **Mechanism** | OS threads (preemptive) | Event loop (cooperative) |
| **Overhead** | Medium (thread creation) | Low (coroutine switching) |
| **Libraries** | Works with `requests`, any sync code | Needs `aiohttp`, `httpx`, async libraries |
| **Gotcha** | GIL limits CPU parallelism | Blocking sync code kills event loop |

> Threading = plug-and-play with existing sync code. AsyncIO = better performance but needs async ecosystem.
</details>

<details>
<summary>❓ Can you mix threading and asyncio?</summary>

Yes! AsyncIO's `asyncio.to_thread()` runs sync functions in a thread pool. Useful when you have blocking sync code (like `requests.get`) inside an async application. Best of both worlds.
</details>

---

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️
