"""
05_pool_map.py — ProcessPoolExecutor + map (start order results)
================================================================
Source: Corey Schafer — Python Multiprocessing Tutorial

- map() runs function over every item in an iterable
- Returns results in START order (not completion order!)
- Unlike submit(), returns results directly (not Future objects)
- Context manager auto-joins — even without iterating results
- Exceptions are raised during iteration, not during execution
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
    results = executor.map(do_something, secs)

    for result in results:
        print(result)

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')
