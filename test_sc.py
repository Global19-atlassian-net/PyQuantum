import sys
from PyQuantum.Tools.LoadPackage import *
from mpi4py import MPI
from time import sleep

config_path = sys.argv[1]
config = load_pkg(config_path, config_path)

print(config.a, config.b)

comm = MPI.COMM_WORLD

mpirank = comm.Get_rank()
mpisize = comm.Get_size()


# 1/0

for i in range(mpisize):
    if i == mpirank:
        print(i, mpisize)

    comm.barrier()

# sleep(100)
