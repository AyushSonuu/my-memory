"""
01_synchronous.py — Baseline: Sequential Execution
===================================================
Source: Corey Schafer — Python Multiprocessing Tutorial
https://www.youtube.com/watch?v=fKl2JW_qrso

Running do_something() twice sequentially → ~2 seconds.
This is the "before" that we'll speed up with multiprocessing.
"""

import time

start = time.perf_counter()


def do_something():
    print('Sleeping 1 second...')
    time.sleep(1)
    print('Done Sleeping...')


do_something()
do_something()

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')
