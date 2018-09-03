"""Parallel map with scheduler distribution jobs as required
"""

from mpi4py import MPI

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

MASTER = 0


def parallel_map(func, mapable, **kwargs):
    """Executes func in parallel for each el in mapable with kwargs.

    The master (rank=0) distributes all the tasks, while the slaves execute the func.
    Each time a slave is ready, the master passes another mapable.
    """

    results = []
    task_order = []
    if not RANK is MASTER:

        task_id = _get_new_task_id()
        while not task_id is None:
            results.append(func(mapable[task_id], **kwargs))
            task_order.append(task_id)
            task_id = _get_new_task_id()

    else:

        todo = list(range(len(mapable)))

        while todo:
            rank = COMM.recv(source=MPI.ANY_SOURCE)
            task_id = todo.pop()
            COMM.isend(task_id, dest=rank, tag=rank)

        # Send break up criterion
        for rank in range(SIZE):
            COMM.isend(None, dest=rank, tag=rank)

    result = []
    index = []
    if MASTER:
        for res in COMM.gather(results, root=MASTER):
            result += res

        for ind in COMM.gather(task_order, root=MASTER):
            index += ind

    return [result[i] for i in index]


def _get_new_task_id():
    """Sends rank to master to get new task id (or None if no open task)
    """
    COMM.send(RANK, dest=MASTER)
    return COMM.recv(source=MASTER)
