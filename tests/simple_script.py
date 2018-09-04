"""Simple test script to visualize how parallel_map works.
"""

from mpischedule.base import RANK
from mpischedule.parallel_map import parallel_map

import time


def func(x, sleep=False):
    if sleep:
        print(f"[{RANK}] func({x})")
        time.sleep(x / 5)
    return x ** 2


if __name__ == "__main__":
    print(f"[{RANK}] Result:", parallel_map(func, range(10), sleep=True))
