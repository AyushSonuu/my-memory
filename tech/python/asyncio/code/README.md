# 💻 AsyncIO — Code Examples

All code from Corey Schafer's AsyncIO tutorial. Click any file to view with syntax highlighting.

## Terms & Terminology

| File | What it covers |
|------|---------------|
| [terms.py](../../../_generated/tech/python/asyncio/code/L1/terms.md) | Sync vs async functions, coroutines, futures, tasks |

## Progressive Examples

| # | File | Concept |
|---|------|---------|
| 1 | [example_1.py](../../../_generated/tech/python/asyncio/code/L1/example_1.md) | Synchronous baseline (3 sec) |
| 2 | [example_2.py](../../../_generated/tech/python/asyncio/code/L1/example_2.md) | Wrong async — awaiting coroutines directly (still 3 sec) |
| 3 | [example_3.py](../../../_generated/tech/python/asyncio/code/L1/example_3.md) | `create_task` — real concurrency (2 sec) ✅ |
| 4 | [example_4.py](../../../_generated/tech/python/asyncio/code/L1/example_4.md) | Await order ≠ execution order |
| 5 | [example_5.py](../../../_generated/tech/python/asyncio/code/L1/example_5.md) | Blocking event loop with `time.sleep` ⛔ |
| 6 | [example_6.py](../../../_generated/tech/python/asyncio/code/L1/example_6.md) | `to_thread` + `ProcessPoolExecutor` |
| 7 | [example_7.py](../../../_generated/tech/python/asyncio/code/L1/example_7.md) | `gather` vs `TaskGroup` |

> 🎨 Interactive animations for each example: [View Animations](../animations/index.html)
