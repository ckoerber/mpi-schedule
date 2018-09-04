# MPI-Schedule
Module for distributing tasks in a master-slave setup.

## Description
This module provides the function `parallel_map` which distributes tasks to several processes.
The master process serves as a scheduler which keeps track of the tasks to execute.
The master distributes tasks to slaves once they signalize free capacities.
Note that the master is not executing the work.
Thus you might want to consider running this script if you have several tasks to distribute which have different runtimes.
Otherwise it might be more useful to plan the distribution and include the master in the workforce.

## Install
Run the following command in this directory
```bash
> pip install -e .
```

## Usage

```python
# simple_script.py
from mpischedule.base import RANK
from mpischedule.parallel_map import parallel_map

import time

def func(x, sleep=False):
    if sleep:
        print(f"[{RANK}] func({x})")
        time.sleep(x/5)
    return x**2

if __name__ == "__main__":
    print(f"[{RANK}] Result:", parallel_map(func, range(10), sleep=True))
```

```bash
> mpirun -n 4 python simple_script.py
[1] func(1)
[1] func(4)
[1] func(7)
[1] Result: None
[3] func(0)
[3] func(3)
[3] func(6)
[3] func(9)
[3] Result: None
[2] func(2)
[2] func(5)
[2] func(8)
[2] Result: None
[0] Result: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```
