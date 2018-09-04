"""Basic definitions of mpischedule module
"""
from mpi4py import MPI

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

MASTER = 0
SLAVE = RANK != MASTER
