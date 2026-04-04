# 💻 Multiprocessing — Code Examples

> Source: [Corey Schafer — Python Multiprocessing Tutorial](https://www.youtube.com/watch?v=fKl2JW_qrso)
> Repo: [CoreyMSchafer/code_snippets/Python/MultiProcessing](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/MultiProcessing)

## L1 — Multiprocessing Complete Guide

| File | What It Shows |
|------|--------------|
| `01_synchronous.py` | Baseline: two `do_something()` calls run sequentially (~2s) |
| `02_basic_processes.py` | Manual `multiprocessing.Process` + `.start()` + `.join()` (~1s, true parallel) |
| `03_loop_processes.py` | 10 processes in a loop with args, join after all start (~1.5s not 15s) |
| `04_pool_submit.py` | `ProcessPoolExecutor.submit()` + `as_completed()` (completion order results) |
| `05_pool_map.py` | `ProcessPoolExecutor.map()` (start order results) |
| `06_process_images.py` | Real-world: blur + resize 15 high-res images (22s sync → 7s parallel) |
