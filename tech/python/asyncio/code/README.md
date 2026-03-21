# 💻 AsyncIO — Code Examples

All code from Corey Schafer's AsyncIO tutorial.

## Terms & Terminology

📄 [terms.py](L1/terms.py) — sync vs async functions, coroutines, futures, tasks

## Progressive Examples

| # | File | Concept |
|---|------|---------|
| 1 | [example_1.py](L1/example_1.py) | Synchronous baseline (3 sec) |
| 2 | [example_2.py](L1/example_2.py) | Wrong async — awaiting coroutines directly (still 3 sec) |
| 3 | [example_3.py](L1/example_3.py) | `create_task` — real concurrency (2 sec) ✅ |
| 4 | [example_4.py](L1/example_4.py) | Await order ≠ execution order |
| 5 | [example_5.py](L1/example_5.py) | Blocking event loop with `time.sleep` ⛔ |
| 6 | [example_6.py](L1/example_6.py) | `to_thread` + `ProcessPoolExecutor` |
| 7 | [example_7.py](L1/example_7.py) | `gather` vs `TaskGroup` |

> 🎨 Interactive animations for each example: [View Animations](../animations/index.html)
