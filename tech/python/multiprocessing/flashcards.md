# 🃏 Multiprocessing Flashcards

> From: multiprocessing/ + related: threading/, asyncio/
> Last updated: 2026-04-04

---

### 📌 Core Multiprocessing

<details markdown="1">
<summary>❓ When should you use multiprocessing over threading?</summary>

| Task Type | Use |
|-----------|-----|
| **CPU-bound** (computation, image filters, math) | ⚙️ Multiprocessing |
| **I/O-bound** (network, disk, sleep) | 🧵 Threading |

Multiprocessing bypasses the GIL → true parallel execution on multiple CPU cores. Threading is limited by the GIL for CPU work.

> CPU heavy = multiprocessing. Waiting heavy = threading. Andha andha mat karo — benchmark karo! 📊
</details>

<details markdown="1">
<summary>❓ What is the GIL and how does multiprocessing bypass it?</summary>

**GIL (Global Interpreter Lock)** = one lock per Python interpreter → only one thread runs Python bytecode at a time.

**Threads** share the interpreter → share the GIL → can't truly run in parallel.
**Processes** = separate Python interpreters → each has its own GIL → true parallel execution.

Multiprocessing = multiple kitchens with multiple chefs. Threading = one kitchen, one chef, fast switching. 👨‍🍳
</details>

<details markdown="1">
<summary>❓ What does "picklable" mean and why do multiprocessing arguments need to be picklable?</summary>

**Pickling** = serializing Python objects into bytes (so they can be reconstructed). Multiprocessing requires it because processes have **separate memory** — arguments must be serialized to pass between processes via IPC.

✅ Picklable: `int`, `float`, `str`, `list`, `dict`, regular functions
❌ Not picklable: lambdas, file handles, database connections, some closures

> Pickle = Python ka courier service. Pack karo → bhejo → unpack karo. Jo pack nahi ho sakta, wo nahi jaata! 📦
</details>

<details markdown="1">
<summary>❓ Why can't you `.join()` inside the process creation loop?</summary>

`.join()` blocks until that process finishes. Inside loop: create P1 → start P1 → **wait for P1** → create P2... = sequential!

**Correct pattern:**
```python
processes = []
for _ in range(10):
    p = multiprocessing.Process(target=fn)
    p.start()
    processes.append(p)        # save reference

for p in processes:            # join AFTER all started
    p.join()
```
</details>

<details markdown="1">
<summary>❓ What happens if you DON'T call `.join()` on your processes?</summary>

Main script continues immediately while processes are still running. Timing/output at the end of the script executes before processes finish — you'll see "Finished in 0 seconds" because processes take time to spin up and main thread just runs past them.

With `ProcessPoolExecutor` context manager: auto-joins when `with` block exits ✅
</details>

<details markdown="1">
<summary>❓ What's the difference between `submit()` and `map()` in ProcessPoolExecutor?</summary>

| | `submit(fn, arg)` + `as_completed()` | `map(fn, iterable)` |
|--|--------------------------------------|---------------------|
| **Returns** | Future objects | Results (generator) |
| **Result order** | ⚡ Completion order (fastest first) | 📋 Start order |
| **Exception** | When `.result()` called | During iteration |
| **Use when** | You want fastest results first | Order matters |

> `as_completed` = race finish line. `map` = roll number order. 🏁📋
</details>

<details markdown="1">
<summary>❓ What is a Future object?</summary>

A `Future` is returned by `executor.submit()`. It **encapsulates the execution** of a function scheduled on a process. You can:
- `.result()` → get return value (blocks until done)
- `.done()` → check if finished
- `.running()` → check if currently executing

It's like a delivery tracking number — submit karo, track karo, result lo. 📬
</details>

<details markdown="1">
<summary>❓ What is the `if __name__ == '__main__':` guard and why is it important for multiprocessing?</summary>

On Windows and macOS (spawn start method), new processes **import the script** to get the function. Without the guard, each spawned process re-runs the main code → infinite process spawning!

```python
if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_image, img_names)
```

Always use this guard in scripts using multiprocessing! In Jupyter notebooks / modules it's usually not needed.
</details>

---

### 🔗 From: Threading (Cross-Topic)

<details markdown="1">
<summary>❓ Threading vs Multiprocessing — full comparison</summary>

| | 🧵 Threading | ⚙️ Multiprocessing |
|--|--------------|---------------------|
| **Parallelism** | Concurrent (overlapping waits) | True parallel (multiple CPUs) |
| **GIL** | Limited by it | Bypasses it ✅ |
| **Best for** | I/O-bound | CPU-bound |
| **Memory** | Shared space | Separate per process |
| **Args requirement** | Any Python object | Must be picklable |
| **Overhead** | Low | High (process spawn) |
| **Switch between them** | Just swap `ThreadPool` ↔ `ProcessPool` | ← same |

Real-world: 15 image downloads → Threading won (I/O-bound). 15 image filters → Multiprocessing 3× faster.
</details>

<details markdown="1">
<summary>❓ Can you switch between ThreadPoolExecutor and ProcessPoolExecutor easily?</summary>

**Yes! That's the beauty of `concurrent.futures`:**

```python
# Multiprocessing:
with concurrent.futures.ProcessPoolExecutor() as executor:

# Threading (one word!):
with concurrent.futures.ThreadPoolExecutor() as executor:
```

Same API: `submit()`, `map()`, `as_completed()` — all identical. Perfect for A/B benchmarking.
</details>

---

### 🔗 From: AsyncIO (Cross-Topic)

<details markdown="1">
<summary>❓ Threading vs Multiprocessing vs AsyncIO — when to use each?</summary>

| | 🧵 Threading | ⚙️ Multiprocessing | ⚡ AsyncIO |
|--|--------------|---------------------|------------|
| **Use when** | I/O, existing sync code | CPU-heavy computation | I/O, high concurrency (1000s) |
| **Mechanism** | OS threads | Separate processes | Single-thread event loop |
| **GIL** | Limited | Bypassed | N/A |
| **Overhead** | Medium | High | Very low |
| **Code style** | Normal Python | Normal Python | `async/await` |

Quick rule: **CPU heavy → multiprocessing. Few I/O calls → threading. Thousands of connections → asyncio.**
</details>

---

> 💡 **Revision tip:** Cover the answer, try to explain OUT LOUD, then reveal.
> Bolke batao — padhke nahi, bolke yaad hota hai! 🗣️
