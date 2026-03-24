# 💻 Threading — Code Examples

> Source: [Corey Schafer — Python Threading Tutorial](https://www.youtube.com/watch?v=IEEhzQoKtQU)
> Repo: [CoreyMSchafer/code_snippets/Python/Threading](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Threading)

## L1 — Threading Complete Guide

| File | What It Shows |
|------|--------------|
| `01_synchronous.py` | Baseline: two `do_something()` calls run sequentially (~2s) |
| `02_basic_threads.py` | Manual `threading.Thread` + `.start()` + `.join()` (~1s) |
| `03_loop_threads.py` | 10 threads in a loop, join after all start (~1.5s not 15s) |
| `04_thread_pool_submit.py` | `ThreadPoolExecutor.submit()` + `as_completed()` (completion order) |
| `05_thread_pool_map.py` | `ThreadPoolExecutor.map()` (start order) |
| `06_download_images.py` | Real-world: download 15 Unsplash images with threads (23s → 5s) |
