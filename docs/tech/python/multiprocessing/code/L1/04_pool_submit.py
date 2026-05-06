"""
04_pool_submit.py — ProcessPoolExecutor + submit + as_completed
===============================================================
Source: Corey Schafer — Python Multiprocessing Tutorial

- submit() schedules a function and returns a Future object
- Future.result() blocks until the process completes
- as_completed() yields futures in COMPLETION order (fastest first!)
- Pool decides how many processes to spawn based on hardware
- Different sleep times prove completion order: 2s→3s→1s→4s→5s
  (1s may be delayed if pool was full and it waited for a slot)
"""

import concurrent.futures
import time

start = time.perf_counter()


def do_something(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return f'Done Sleeping...{seconds}'


with concurrent.futures.ProcessPoolExecutor() as executor:
    secs = [5, 4, 3, 2, 1]
    results = [executor.submit(do_something, sec) for sec in secs]

    for f in concurrent.futures.as_completed(results):
        print(f.result())

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')
