"""
02_basic_processes.py — Manual multiprocessing.Process
======================================================
Source: Corey Schafer — Python Multiprocessing Tutorial

Create two Process objects, start them, and join them.
Without join() → main script finishes in 0s (processes still running).
With join() → waits for both → ~1 second total (true parallel!).

Key difference from threading: processes actually run on separate CPUs.
Processes take longer to spin up than threads.
"""

import multiprocessing
import time

start = time.perf_counter()


def do_something():
    print('Sleeping 1 second...')
    time.sleep(1)
    print('Done Sleeping...')


# Create process objects (not running yet!)
p1 = multiprocessing.Process(target=do_something)
p2 = multiprocessing.Process(target=do_something)

# Start them (now they actually run on separate CPU cores)
p1.start()
p2.start()

# Wait for both to finish before continuing
p1.join()
p2.join()

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')
