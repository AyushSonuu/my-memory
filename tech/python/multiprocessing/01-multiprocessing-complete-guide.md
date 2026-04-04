# 01 · Multiprocessing — True Parallelism in Python ⚙️

---

## 🎯 One Line
> Multiprocessing runs tasks on **separate CPU cores simultaneously** — true parallelism, not just concurrency. Perfect for CPU-bound tasks where threading's GIL is a dead end.

---

## 🖼️ Sync vs Parallel Execution

```
┌─────────────────────────────────────────────────────────┐
│  🐌 SYNCHRONOUS                                          │
│                                                          │
│  ──▶ func()──[1s]──▶ func()──[1s]──▶ done              │
│  Total: ~2 seconds                                       │
├──────────────────────────────────────────────────────────┤
│  🧵 THREADED (concurrent, not parallel)                  │
│                                                          │
│  ──▶ func()──[1s]──┐                                     │
│  ──▶ func()──[1s]──┤ ← overlapped, but SAME CPU         │
│  Total: ~1 second  ▼                                     │
│            GIL limits true parallelism ⚠️                │
├──────────────────────────────────────────────────────────┤
│  ⚙️ MULTIPROCESSING (true parallelism)                   │
│                                                          │
│  CPU Core 1 ──▶ func()──[1s]──┐                          │
│  CPU Core 2 ──▶ func()──[1s]──┤ ← DIFFERENT CPUs!       │
│  Total: ~1 second              ▼                         │
│                            GIL bypassed ✅               │
└──────────────────────────────────────────────────────────┘
```

> 💡 **Threading = ek chef, multiple burners (saath kaam karta hai but ek hi insaan). Multiprocessing = multiple chefs, multiple kitchens — sach mein parallel! 👨‍🍳👨‍🍳👨‍🍳**

---

## 🧱 Threading vs Multiprocessing — Pick Your Weapon

| | 🧵 Threading | ⚙️ Multiprocessing |
|--|--------------|---------------------|
| **True parallelism** | ❌ No (GIL limits) | ✅ Yes (separate processes) |
| **Best for** | I/O-bound (network, disk, sleep) | CPU-bound (computation, processing) |
| **Overhead** | Low (thread creation) | High (process creation + memory) |
| **Memory** | Shared memory space | Separate memory per process |
| **Argument passing** | Any Python object | Must be **picklable** |
| **Startup cost** | Fast | Slower (process spin-up takes time) |
| **GIL** | Limited by it | Bypasses it ✅ |

> 💡 **I/O-bound = threading. CPU-bound = multiprocessing. Mix karo → benchmark karo. Andha andha koi kaam nahi! 🔬**

---

## 🧱 What is CPU-bound vs I/O-bound?

| Type | What It Means | Examples |
|------|--------------|---------|
| **CPU-bound** | CPU is maxed out crunching numbers | Image filters, data analysis, cryptography, ML inference |
| **I/O-bound** | CPU is mostly idle, waiting for external ops | HTTP requests, file read/write, `time.sleep`, DB queries |

> ⚠️ Threading on CPU-bound = SLOWER than sequential (thread overhead + GIL fighting)

---

## ⚡ Method 1: Manual `multiprocessing.Process`

### The Old-School Way — Good to Understand Internals

```python
import multiprocessing
import time

def do_something(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return f'Done Sleeping...{seconds}'

# Create process objects (not running yet!)
p1 = multiprocessing.Process(target=do_something, args=[1])
p2 = multiprocessing.Process(target=do_something, args=[1])

# Start them (now they actually run)
p1.start()
p2.start()

# Wait for both to finish BEFORE continuing
p1.join()
p2.join()

# Result: ~1 second (not 2!)
```

> ⚠️ **Without `.join()`:** main script prints "Finished in 0 seconds" before processes even start their sleep — processes take time to spin up!

### Loop — 10 Processes

```python
processes = []

for _ in range(10):
    p = multiprocessing.Process(target=do_something, args=[1.5])
    p.start()
    processes.append(p)    # save reference!

for process in processes:  # join AFTER all started!
    process.join()

# 10 × 1.5s sync = 15s → with multiprocessing: ~1.5s 🔥
```

> ⚠️ **Don't `.join()` inside the creation loop!** Same trap as threading — it would make each process finish before starting the next = sequential. Start all → then join all.

### Key API

| | What It Does |
|--|-------------|
| `Process(target=fn, args=[...])` | Create process object (NOT running yet). **No `()` on fn!** |
| `.start()` | Launch the process on a separate CPU core |
| `.join()` | Main thread waits until this process finishes |
| `args=[...]` | Must be **picklable** Python objects |

### Pickle Requirement ⚠️

```python
# Arguments to multiprocessing.Process MUST be picklable
# (Can be serialized/deserialized across processes)

# ✅ Picklable: int, float, str, list, dict, tuple
p = multiprocessing.Process(target=fn, args=[1.5])       # ✅
p = multiprocessing.Process(target=fn, args=["hello"])   # ✅

# ❌ Not picklable: lambda functions, file handles, database connections
p = multiprocessing.Process(target=lambda: fn())         # ❌ (usually)
```

> 💡 **Pickle = Python ka courier service. Ek Python script ka object dusri Python script mein bhejne ke liye pehle pack karo (serialize), phir unpack karo (deserialize). Jo pack nahi ho sakta, wo bhej nahi sakte! 📦**

---

## ⚡ Method 2: `ProcessPoolExecutor` (Modern, Preferred)

> Added in Python 3.2 via `concurrent.futures`. Cleaner, smarter, and easy to switch between processes/threads.

```python
import concurrent.futures
```

### `submit()` — One at a Time, Returns Future

```python
with concurrent.futures.ProcessPoolExecutor() as executor:
    f1 = executor.submit(do_something, 1)
    f2 = executor.submit(do_something, 2)
    
    print(f1.result())   # blocks until process finishes
    print(f2.result())

# Both kick off in parallel, finish in ~2s (not 3s)
```

| Concept | What It Is |
|---------|-----------|
| **`submit(fn, *args)`** | Schedules function on a process, returns **Future** |
| **Future** | Encapsulates execution — check `.running()`, `.done()`, `.result()` |
| **`.result()`** | Blocks until complete, returns the function's return value |

> 💡 **Future object = delivery tracking number. Submit karo → tracking mile ga. `.result()` = "Kahan hai mera parcel?" — wait karo jab tak na aaye! 📬**

### `submit()` + `as_completed()` — Results in Completion Order

```python
with concurrent.futures.ProcessPoolExecutor() as executor:
    secs = [5, 4, 3, 2, 1]
    futures = [executor.submit(do_something, sec) for sec in secs]

    for f in concurrent.futures.as_completed(futures):
        print(f.result())

# Prints in order: 1s → 2s → 3s → 4s → 5s  (fastest first!)
```

### `map()` — Run Over a List, Results in Start Order

```python
with concurrent.futures.ProcessPoolExecutor() as executor:
    secs = [5, 4, 3, 2, 1]
    results = executor.map(do_something, secs)

    for result in results:
        print(result)

# Prints in order: 5s → 4s → 3s → 2s → 1s  (start order, not completion!)
# But total time is still ~5s (all ran in parallel)
```

---

## 📊 submit vs map — The Key Difference

| | `submit()` + `as_completed()` | `map()` |
|--|-------------------------------|---------|
| **Returns** | Future objects | Results directly (generator) |
| **Result order** | ⚡ **Completion order** (fastest first) | 📋 **Start order** (as submitted) |
| **Exception** | Raised when `.result()` called | Raised during iteration |
| **Use case** | When you want fastest results first | When order matters |

> 💡 **`as_completed` = race — jo pehle finish kare, uska result pehle aaye. `map` = exam result — chahe Raju fast tha, roll number order mein hi aayega! 🏁📋**

---

## 🔄 The Pool Magic — How Many Processes?

```
ProcessPoolExecutor — lets the pool decide (usually = number of CPU cores)
                 ┌─────────────────────────────────────┐
You submit 10    │  Core 1: Process 1 (5s)              │
tasks but have   │  Core 2: Process 2 (4s)              │
4 CPU cores:     │  Core 3: Process 3 (3s)              │
                 │  Core 4: Process 4 (2s)              │
                 │  ← when P4 finishes → Process 5(1s)  │
                 └─────────────────────────────────────┘
```

> The pool intelligently queues tasks. With 4 cores and 5 tasks: 4 start immediately, 5th starts when any of the first 4 finishes.

```python
# You can specify manually if needed:
with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    ...
```

---

## 🌐 Real-World Example: Image Processing

### The Problem — 15 High-Res Photos, Synchronous: **22 seconds** 🐌

```python
from PIL import Image, ImageFilter

img_names = ['photo1.jpg', 'photo2.jpg', ...]  # 15 images
size = (1200, 1200)

for img_name in img_names:
    img = Image.open(img_name)
    img = img.filter(ImageFilter.GaussianBlur(15))   # CPU work
    img.thumbnail(size)                               # resize
    img.save(f'processed/{img_name}')
    print(f'{img_name} processed')

# Sequential: 22 seconds 😴
```

### With Multiprocessing: **7 seconds** ⚡ (3× faster!)

**The trick:** Extract loop body → function, then `ProcessPoolExecutor.map()`

```python
import concurrent.futures
from PIL import Image, ImageFilter

img_names = ['photo1.jpg', 'photo2.jpg', ...]
size = (1200, 1200)

def process_image(img_name):               # ← extracted function
    img = Image.open(img_name)
    img = img.filter(ImageFilter.GaussianBlur(15))
    img.thumbnail(size)
    img.save(f'processed/{img_name}')
    print(f'{img_name} processed')

with concurrent.futures.ProcessPoolExecutor() as executor:
    executor.map(process_image, img_names) # ← one line change!

# Multiprocessing: 7 seconds 🔥
```

```
┌────────────────────────────────────────────────┐
│  🐌 Sequential:  15 images × ~1.5s each        │
│  ════════════════════════════════  22 seconds   │
├────────────────────────────────────────────────┤
│  ⚙️ Multiprocessing: parallel on all cores     │
│  ════════════  7 seconds  (3× faster!)         │
└────────────────────────────────────────────────┘
```

### But Wait — Test Both!

```python
# Switch to ThreadPoolExecutor with ONE word change:
with concurrent.futures.ThreadPoolExecutor() as executor:  # ← just this!
    executor.map(process_image, img_names)

# Result: 7.2 seconds — even faster than multiprocessing!
```

> **Why?** Image processing (opening/saving files) is mostly I/O-bound, not CPU-bound. Threading was actually better here. **Always benchmark — don't assume!**

> 💡 **Pehle andaza lagao, phir test karo. Rule of thumb: CPU heavy → multiprocessing, Waiting heavy → threading. But data hi bolta hai sach! 📊**

---

## 🔄 Context Manager Auto-Joins

```python
with concurrent.futures.ProcessPoolExecutor() as executor:
    results = executor.map(do_something, secs)
    # Even if you don't iterate results here...

# ← When `with` block exits, ALL processes are automatically joined!
# Main script waits here until all finish, even without explicit .join()
```

> ⚠️ **Exceptions in `map()` or `submit()`:** Not raised during execution. Raised only when you retrieve the result (call `.result()` or iterate `map()`).

---

## 🔑 Complete API Cheat Sheet

| What | How | Notes |
|------|-----|-------|
| **Create process** | `multiprocessing.Process(target=fn, args=[...])` | No `()` on fn! |
| **Start** | `p.start()` | Launches process |
| **Wait** | `p.join()` | After ALL starts, not inside loop |
| **Pool (preferred)** | `concurrent.futures.ProcessPoolExecutor()` | Use as context manager |
| **Submit one** | `executor.submit(fn, arg)` | Returns Future |
| **Get result** | `future.result()` | Blocks until done |
| **Results ASAP** | `as_completed(futures)` | Completion order |
| **Map over list** | `executor.map(fn, iterable)` | Start order, auto-parallel |
| **Custom workers** | `ProcessPoolExecutor(max_workers=4)` | Default = CPU count |
| **Thread switch** | Replace `Process` → `Thread` Pool | One word, same API! |

---

## ⚠️ Gotchas

- ❌ **`()` on target function** — `Process(target=fn())` executes immediately, passes return value (None) instead of function
- ❌ **`.join()` inside creation loop** — makes it sequential again
- ❌ **Non-picklable arguments** — lambda functions, file handles, etc. cause `PicklingError`
- ❌ **Using multiprocessing for I/O-bound** — not necessarily faster than threading; benchmark first!
- ❌ **Spawning too many processes** — process creation overhead is significant; pool manages this, but setting `max_workers=1000` would hurt
- ⚠️ **macOS/Windows + `if __name__ == '__main__':`** — on some platforms, multiprocessing code MUST be inside this guard to prevent infinite process spawning

```python
# ✅ Safe pattern for scripts (especially on Windows/macOS):
if __name__ == '__main__':
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(process_image, img_names)
```

---

## 🔗 Threading vs Multiprocessing vs AsyncIO — Full Picture

| | 🧵 Threading | ⚙️ Multiprocessing | ⚡ AsyncIO |
|--|--------------|---------------------|------------|
| **Parallelism** | Concurrent (fake parallel) | True parallel | Concurrent (fake parallel) |
| **Best for** | I/O-bound | CPU-bound | I/O-bound (high concurrency) |
| **GIL** | Limited by it | Bypasses it | N/A (single thread) |
| **Memory** | Shared | Separate (isolated) | Shared |
| **Overhead** | Medium | High (process spawn) | Very low |
| **Switch to other** | `ProcessPoolExecutor` | `ThreadPoolExecutor` | Manual refactor |
| **Real-world speedup** | 15 downloads: 23s→5s | 15 images: 22s→7s | Best for 1000s connections |

> 💡 **Threading = ek chef, multiple burners. Multiprocessing = multiple chefs, multiple kitchens. AsyncIO = ek superfast waiter who never waits — jo free, usse serve karo! 🍳🏨**

---

## 🧪 Quick Check

<details>
<summary>❓ Why does multiprocessing bypass the GIL but threading doesn't?</summary>

The **GIL (Global Interpreter Lock)** is per-interpreter. Threads share the same Python interpreter → same GIL → only one thread runs Python code at a time. Processes are entirely separate Python interpreters, each with their own GIL → can truly run in parallel on multiple CPU cores.
</details>

<details>
<summary>❓ What does "picklable" mean, and why does multiprocessing require it?</summary>

**Pickling** = serializing a Python object into bytes (like JSON but for Python objects). Multiprocessing requires it because processes have **separate memory spaces** — arguments must be serialized, sent via IPC (inter-process communication), and deserialized in the new process. Threads share memory so no serialization needed. Things like lambdas and file handles can't be pickled.
</details>

<details>
<summary>❓ What's the difference between `submit()` and `map()` in ProcessPoolExecutor?</summary>

`submit(fn, arg)` → schedules ONE call, returns a **Future** (use with `as_completed()` for completion-order results).

`map(fn, iterable)` → schedules fn for EVERY item in iterable, returns results in **start order** (not completion order).

Rule: Want fastest-first? → `submit + as_completed`. Want order preserved? → `map`.
</details>

<details>
<summary>❓ Can you just swap ProcessPoolExecutor with ThreadPoolExecutor for the same code?</summary>

**Yes!** The `concurrent.futures` API is identical for both. `executor.submit()`, `executor.map()`, `as_completed()` — all work the same way. Just change one word:

```python
# Multiprocessing:
with concurrent.futures.ProcessPoolExecutor() as executor:

# Threading (one word change!):
with concurrent.futures.ThreadPoolExecutor() as executor:
```

This is the **best argument for using `concurrent.futures`** — easy A/B testing.
</details>

<details>
<summary>❓ Image processing went from 22s → 7s with multiprocessing, but threads were actually faster (7.2s). Why?</summary>

Despite doing image filters/resizing (seemingly CPU work), the bottleneck was opening and saving files — which is **I/O-bound** (disk operations). Threading handles I/O-bound tasks better because threads can overlap during I/O waits without the overhead of spawning separate processes. Multiprocessing's process creation cost partially offset its gains here. **Lesson: always benchmark with real data!**
</details>

---

> **Related →** [Threading](../threading/01-threading-complete-guide.md) · [AsyncIO](../asyncio/01-asyncio-complete-guide.md)
