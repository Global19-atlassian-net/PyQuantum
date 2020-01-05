from mpi4py import MPI

comm = MPI.COMM_WORLD

mpirank = comm.Get_rank()
mpisize = comm.Get_size()

nt_batch = 20

print(mpirank, mpisize)
