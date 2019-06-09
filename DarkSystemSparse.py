import PyQuantum.DarkState.operators as op
from PyQuantum.DarkState.config import *
from PyQuantum.Common.Matrix import *
from scipy import sparse
import copy
from scipy.linalg.interpolative import *
import math
import sys
from scipy.sparse import vstack, hstack
from scipy.sparse.linalg import *

# ---------------------------


class bits:
    def __init__(self, size, n_levels):
        self.n = size
        self.n_levels = n_levels
        self.data = [0] * self.n

    def inc(self):
        inced = False

        for i in range(self.n-1, -1, -1):
            if self.data[i] < self.n_levels-1:
                self.data[i] += 1
                inced = True
                break
            else:
                self.data[i] = 0

        return inced

    def print(self):
        print(self.data)


def to_n(n, n_levels):
    if n == 0:
        return [[0]]

    bitsize = math.ceil(math.log(n+1)/math.log(n_levels))

    d = bits(size=bitsize, n_levels=n_levels)

    arr = []

    cnt = 1

    while True:
        arr.append(copy.copy(d.data))

        if cnt > n or not d.inc():
            break

        cnt += 1

    return arr


def get_system1(n_levels, n_atoms):
    Sigma_ij = None

    DIM = math.pow(n_levels, n_atoms)
    DIM = int(DIM)

    for i in range(0, n_levels):
        for j in range(0, i):
            s_ij = None

            for i_atom in range(1, n_atoms+1):
                # -----------------------------------------------------------------------------------------
                s = op.Sigma2(i_=i, j_=j, num=i_atom,
                              n_atoms=n_atoms, n_levels=n_levels)

                if s_ij is None:
                    s_ij = s
                else:
                    s_ij += s
                # -----------------------------------------------------------------------------------------

            Sigma_ij = s_ij

            m_, n_ = np.shape(Sigma_ij)

            print('m =', m_, ', n =', n_)
            mat = Sigma_ij.todense()

            rg = np.linalg.matrix_rank(mat)

            print('rg = ', rg, ', n = ', n_, ', dim = ', n_ - rg, sep='')
            # for i in mat:
            # print(i)
            return n_ - rg
    return 1


def get_system2(n_levels, n_atoms):
    Sigma_ij = None
    Sigma_ij_t = None

    DIM = math.pow(n_levels, n_atoms)
    DIM = int(DIM)

    # ab = to_n(DIM-1, n_levels)

    for i in range(0, n_levels):
        for j in range(0, i):
            # print('σ(', i, ',', j, '):', sep='')

            s_ij = None
            s_ij_t = None

            for i_atom in range(1, n_atoms+1):
                # -----------------------------------------------------------------------------------------
                s = op.Sigma2(i_=i, j_=j, num=i_atom,
                              n_atoms=n_atoms, n_levels=n_levels)
                # print(np.shape(s))
                # st = np.transform(s)
                # st = op.Sigma2T(i_=i, j_=j, num=i_atom,
                # n_atoms=n_atoms, n_levels=n_levels)

                if s_ij is None:
                    s_ij = s
                    # s_ij_t = st
                else:
                    s_ij += s

                    # s_ij_t += st
                # -----------------------------------------------------------------------------------------

            # if Sigma_ij is None:
            Sigma_ij = s_ij
            # Sigma_ij_t = s_ij_t
            # else:
            # Sigma_ij = vstack((Sigma_ij, s_ij))
            # Sigma_ij_t = vstack((Sigma_ij_t, s_ij_t))

            # Sigma_ij = vstack((Sigma_ij, Sigma_ij_t))

            m_, n_ = np.shape(Sigma_ij)
            print('m =', m_, ', n =', n_)
            # print('size:', sys.getsizeof(min(m_, n_)-1)
            # u, s, vt = svds(Sigma_ij, k=min(m_, n_-1))

            mat = Sigma_ij.todense()
            # print(mat)
            # for i in mat:
            # print(','.join([str(elem) for elem in i]))
            # print()

            rg = np.linalg.matrix_rank(mat)
            # print('rank_dense=', rg_ok)

            print('rg = ', rg, ', n = ', n_, ', dim = ', n_ - rg, sep='')

    return 1
    # return n_ - rg
