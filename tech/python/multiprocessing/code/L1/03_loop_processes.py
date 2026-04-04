"""
03_loop_processes.py — 10 Processes in a Loop (with args)
=========================================================
Source: Corey Schafer — Python Multiprocessing Tutorial

- Creates 10 processes in a loop, each sleeping 1.5s
- Appends to list, then joins all AFTER starting
- DON'T join inside the loop — that makes it sequential!
- Arguments via args=[...] — MUST be picklable (serializable)
- Result: ~1.5s instead of 15s synchronous
"""

import multiprocessing
import time

start = time.perf_counter()


def do_something(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    print(f'Done Sleeping...{seconds}')


processes = []

for _ in range(10):
    p = multiprocessing.Process(target=do_something, args=[1.5])
    p.start()
    processes.append(p)

for process in processes:
    process.join()

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')
