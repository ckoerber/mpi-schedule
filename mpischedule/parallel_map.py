"""Parallel map with scheduler distribution jobs as required
"""
from typing import Callable
from typing import List

from mpischedule.base import MPI
from mpischedule.base import COMM
from mpischedule.base import RANK
from mpischedule.base import SIZE
from mpischedule.base import MASTER
from mpischedule.base import IS_SLAVE
from mpischedule.base import IS_MASTER


def parallel_map(func: Callable, iteratable: List, **kwargs) -> List:
    """Executes func in parallel for each el in iteratable. Kwargs are passed to func.

    The master (rank=0) distributes all the tasks, while the slaves execute the func.
    Each time a slave is ready, the master distributes another element of iteratable.

    Return values of func are passed put on master.
    """
    if SIZE == 1:
        raise ValueError("Script needs at least 2 process to run.")

    results = []
    task_order = []

    if IS_SLAVE:

        task_id = _get_new_task_id()
        while not task_id is None:
            results.append(func(iteratable[task_id], **kwargs))
            task_order.append(task_id)
            task_id = _get_new_task_id()

    else:

        todo = list(range(len(iteratable)))
        while todo:
            rank = COMM.recv(source=MPI.ANY_SOURCE)
            task_id = todo.pop(0)
            COMM.isend(task_id, dest=rank, tag=rank)

        # Send break up criterion
        for rank in range(SIZE):
            COMM.isend(None, dest=rank, tag=rank)

    out = None
    local_res = COMM.gather(results, root=MASTER)
    local_ind = COMM.gather(task_order, root=MASTER)
    if IS_MASTER:
        result = []
        for res in local_res:
            result += res

        index = []
        for ind in local_ind:
            index += ind

        out = [result[i] for i in index]

    return out


def _get_new_task_id():
    """Sends rank to master to get new task id (or None if no open task)
    """
    COMM.send(RANK, dest=MASTER)
    return COMM.recv(source=MASTER)
