# 01 · Threading — Run Code Concurrently 🧵

---

## 🎯 One Line
> Threading lets your Python program do other work while waiting for I/O (network, disk, sleep) — it's **concurrency** (not parallelism), and it's perfect for I/O-bound tasks.

---

## 🖼️ Sync vs Threaded Execution

```
┌─────────────────────────────────────────────────┐
│  🐌 SYNCHRONOUS (no threading)                   │
│                                                  │
│  ──▶ func()──[sleep 1s]──▶ func()──[sleep 1s]── │
│  Total: ~2 seconds                               │
├──────────────────────────────────────────────────┤
│  ⚡ THREADED (concurrent)                        │
│                                                  │
│  ──▶ func()──[sleep 1s]──────┐                   │
│  ──▶ func()──[sleep 1s]──────┤  ← overlapped!   │
│  Total: ~1 second            ▼                   │
│                            Done!                 │
└──────────────────────────────────────────────────┘
```

> 💡 **Threading = multitasking, not parallel processing. Jaise tum washing machine chala ke bartan dhone lag gaye — dono saath ho rahe hain but TUM ek hi ho. CPU ek hai, lekin idle time mein doosra kaam kar liya!** 🧺🍽️

---

## 🧱 When To Use What

| Task Type | Description | Examples | Best Tool |
|-----------|-------------|----------|-----------|
| **I/O-bound** | Waiting for input/output, CPU mostly idle | Network requests, file read/write, `time.sleep` | 🧵 **Threading** |
| **CPU-bound** | Heavy computation, CPU maxed out | Image processing, number crunching, data analysis | ⚙️ **Multiprocessing** |

> ⚠️ Threading on CPU-bound tasks can be **SLOWER** than sequential — thread creation/destruction overhead adds up with zero benefit.

---

## ⚡ Method 1: Manual Threads (`threading` module)

### Basic — Two Threads

```python
import threading
import time

def do_something():
    print('Sleeping 1 second...')
    time.sleep(1)
    print('Done Sleeping...')

t1 = threading.Thread(target=do_something)  # don't add () to function!
t2 = threading.Thread(target=do_something)

t1.start()   # kicks off the thread
t2.start()

t1.join()    # wait for t1 to finish before continuing
t2.join()

# Result: ~1 second (not 2!)
```

| Method | What It Does |
|--------|-------------|
| `Thread(target=fn)` | Creates thread (does NOT run it). **No parentheses on fn!** |
| `.start()` | Actually runs the thread |
| `.join()` | Blocks until thread finishes — ensures completion before moving on |

> ⚠️ Without `.join()`, the main script continues immediately while threads are still sleeping — you'll see "Finished in 0 seconds" before threads print "Done"!

### Loop — 10 Threads

```python
threads = []

for _ in range(10):
    t = threading.Thread(target=do_something, args=[1.5])
    t.start()
    threads.append(t)

for thread in threads:    # join AFTER all started!
    thread.join()

# 10 × 1.5s synchronously = 15 seconds
# With threads = 1.5 seconds! 🔥
```

> ⚠️ **Don't `.join()` inside the creation loop!** That would wait for each thread to finish before starting the next = same as synchronous. Start all first, then join all.

### Passing Arguments

```python
# args takes a list
t = threading.Thread(target=do_something, args=[1.5])
```

---

## ⚡ Method 2: ThreadPoolExecutor (`concurrent.futures`)

> Added in Python 3.2. Easier, cleaner, and auto-manages thread lifecycle. This is the **preferred way**.

### `submit()` — One at a Time, Returns Future

```python
import concurrent.futures

def do_something(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return f'Done Sleeping...{seconds}'

with concurrent.futures.ThreadPoolExecutor() as executor:
    f1 = executor.submit(do_something, 1)  # returns Future object
    print(f1.result())  # blocks until done, returns return value
```

| Concept | What It Is |
|---------|-----------|
| **`submit(fn, *args)`** | Schedules function, returns **Future** object |
| **Future** | Encapsulates execution — check `.running()`, `.done()`, `.result()` |
| **`.result()`** | Blocks until complete, returns the function's return value |

### `submit()` + `as_completed()` — Results in Completion Order

```python
with concurrent.futures.ThreadPoolExecutor() as executor:
    secs = [5, 4, 3, 2, 1]
    futures = [executor.submit(do_something, sec) for sec in secs]

    for f in concurrent.futures.as_completed(futures):
        print(f.result())
# Prints: 1s → 2s → 3s → 4s → 5s  (fastest finishes first!)
```

### `map()` — Results in Start Order

```python
with concurrent.futures.ThreadPoolExecutor() as executor:
    secs = [5, 4, 3, 2, 1]
    results = executor.map(do_something, secs)

    for result in results:
        print(result)
# Prints: 5s → 4s → 3s → 2s → 1s  (order submitted, NOT completed)
```

---

## 📊 submit vs map — The Key Difference

| | `submit()` + `as_completed()` | `map()` |
|--|-------------------------------|---------|
| **Returns** | Future objects | Results directly |
| **Result order** | ⚡ **Completion order** (fastest first) | 📋 **Start order** (as submitted) |
| **Exception handling** | Exception raised when `.result()` called | Exception raised during iteration |
| **Use case** | When you care about fast results first | When order matters |

> 💡 **`as_completed` = race finish line (jo pehle aaya, uska result pehle). `map` = exam roll number order (chahe late submit karo, number sequence mein hi aayega)!** 🏁

---

## 🌐 Real-World Example: Download 15 Images

### Without Threading — 23 seconds 🐌

```python
for img_url in img_urls:        # 15 URLs
    img_bytes = requests.get(img_url).content
    # save to file...
# Downloads one at a time, waits for each response
```

### With Threading — 5 seconds ⚡

```python
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(download_image, img_urls)
# All 15 requests fire concurrently!
```

```
┌──────────────────────────────────────────────┐
│  🐌 Sequential: 15 images × ~1.5s each       │
│  ════════════════════════════════════  23s    │
├──────────────────────────────────────────────┤
│  ⚡ Threaded: 15 images concurrently         │
│  ═══════  5s  (~4.6× faster!)               │
└──────────────────────────────────────────────┘
```

> The more I/O-bound operations you have, the bigger the speedup!

---

## 📋 Complete Cheat Sheet

| What | How | Notes |
|------|-----|-------|
| **Create thread** | `threading.Thread(target=fn, args=[...])` | Don't add `()` to fn! |
| **Start** | `t.start()` | Kicks off execution |
| **Wait for finish** | `t.join()` | Call after ALL starts, not inside loop |
| **Pool (preferred)** | `concurrent.futures.ThreadPoolExecutor()` | Use as context manager |
| **Submit one** | `executor.submit(fn, arg)` | Returns Future |
| **Get result** | `future.result()` | Blocks until done |
| **Results ASAP** | `as_completed(futures)` | Yields in completion order |
| **Map over list** | `executor.map(fn, iterable)` | Returns in start order |
| **Context manager** | `with ... as executor:` | Auto-joins all threads at end |

---

## ⚠️ Gotchas

- ❌ **Putting `()` on target function** — `Thread(target=do_something())` EXECUTES the function immediately instead of passing it
- ❌ **`.join()` inside creation loop** — makes it synchronous again
- ❌ **Using threads for CPU-bound work** — use `multiprocessing` instead (GIL blocks true parallelism)
- ❌ **Forgetting `.join()`** — main script finishes before threads, timing/output is wrong
- ⚠️ **Exceptions in `map()`** — raised only when iterating results, not when thread runs

---

## 🔗 Threading vs AsyncIO vs Multiprocessing

| | Threading | AsyncIO | Multiprocessing |
|--|-----------|---------|-----------------|
| **Best for** | I/O-bound | I/O-bound | CPU-bound |
| **Mechanism** | OS threads | Single-thread event loop | Separate processes |
| **GIL** | Limited by GIL | N/A (single thread) | Bypasses GIL ✅ |
| **Syntax** | `threading.Thread` / `ThreadPoolExecutor` | `async/await` | `multiprocessing.Process` / `ProcessPoolExecutor` |
| **Overhead** | Medium (thread creation) | Low (coroutine switching) | High (process creation) |

> 💡 **Threading = kitchen mein ek chef, multiple burners (ek ek karke check karta hai). AsyncIO = same but waiter style (order le, kitchen bhejo, next customer). Multiprocessing = multiple chefs, multiple kitchens! 👨‍🍳👨‍🍳👨‍🍳**

---

## 🧪 Quick Check

<details>
<summary>❓ Why doesn't threading make CPU-bound tasks faster?</summary>

Because of Python's **GIL (Global Interpreter Lock)** — only one thread can execute Python bytecode at a time. For CPU-bound tasks, threads just take turns using the CPU with added overhead. Use `multiprocessing` instead which runs separate processes, each with their own GIL.
</details>

<details>
<summary>❓ What's the difference between `submit()` and `map()`?</summary>

`submit()` returns **Future objects** — use with `as_completed()` to get results in **completion order** (fastest first). `map()` returns results directly in **start order** (same order as input iterable). Both run threads concurrently.
</details>

<details>
<summary>❓ Why must `.join()` be called AFTER all `.start()` calls?</summary>

`.join()` blocks the main thread until that thread finishes. If you join inside the creation loop, each thread must finish before the next one starts — defeating the entire purpose of threading. **Start all, then join all.**
</details>

<details>
<summary>❓ What happens if you don't call `.join()` at all?</summary>

The main script continues executing while threads are still running. Your timing/print statements at the end will execute before threads finish. With `ThreadPoolExecutor` as a context manager, this is handled automatically — it joins all threads when the `with` block exits.
</details>

---

> **Related →** [AsyncIO](../asyncio/01-asyncio-complete-guide.md) · Multiprocessing (coming next!)
