import PyQuantum.DarkState.operators as op
from PyQuantum.DarkState.config import *
from PyQuantum.Common.Matrix import *
from scipy import sparse
import copy
from scipy.linalg.interpolative import *
import math
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

    # print(bitsize)

    d = bits(size=bitsize, n_levels=n_levels)

    arr = []

    cnt = 1

    while True:
        # d.print()
        arr.append(copy.copy(d.data))

        if cnt > n or not d.inc():
            break

        cnt += 1

    return arr


def get_system2(n_levels, n_atoms):
    print(123)
    return 666
    Sigma_ij = None
    Sigma_ij_t = None

    DIM = math.pow(n_levels, n_atoms)
    # print(DIM)
    DIM = int(DIM)

    ab = to_n(DIM-1, n_levels)

    for i in range(0, n_levels):
        for j in range(0, i):
            # print('σ(', i, ',', j, '):', sep='')

            s_ij = None
            s_ij_t = None

            for i_atom in range(1, n_atoms+1):
                # -----------------------------------------------------------------------------------------
                s = op.Sigma2(i_=i, j_=j, num=i_atom,
                              n_atoms=n_atoms, n_levels=n_levels)
                st = op.Sigma2T(i_=i, j_=j, num=i_atom,
                                n_atoms=n_atoms, n_levels=n_levels)
                # st = np.transpose(copy.copy(s))

                if s_ij is None:
                    s_ij = s
                    s_ij_t = st
                else:
                    s_ij += s

                    s_ij_t += st
                # -----------------------------------------------------------------------------------------

            if Sigma_ij is None:
                Sigma_ij = s_ij
                Sigma_ij_t = s_ij_t
            else:
                # print(s_ij)
                Sigma_ij = vstack((Sigma_ij, s_ij))
                # Sigma_ij = np.concatenate((Sigma_ij, s_ij), axis=0)
                # Sigma_ij_t = np.concatenate((Sigma_ij_t, s_ij_t), axis=0)
                Sigma_ij_t = vstack((Sigma_ij_t, s_ij_t))
                # ab = np.concatenate((ab, copy.copy(ab)), axis=0)
                # ab = hstack((ab, copy.copy(ab)))

    # for i in ab:
    # print(i)
    # print(Sigma_ij)
    # Sigma_ij = vstack((Sigma_ij, Sigma_ij_t))
    # Sigma_ij = np.concatenate((Sigma_ij, Sigma_ij_t), axis=0)
    # ab = np.concatenate((ab, copy.copy(ab)), axis=0)
    # ab = hstack((ab, copy.copy(ab)))

    m_, n_ = np.shape(Sigma_ij)
    print(123)
    for i in self.data:
        print(i)
    # Stigma_ij = Matrix(m=m_, n=n_, dtype=int)
    # Stigma_ij.data = Sigma_ij
    # for i in Stigma_ij.data:
    # print(''.join([str(int(t)) for t in i]))
    # print(Stigma_ij.m, np.linalg.matrix_rank(Stigma_ij.data), Stigma_ij.n)
    # mat = Sigma_ij.todense()
    # print(np.shape(mat))
    # print('rank=', np.linalg.matrix_rank(mat),

    # u, s, vt = svds(Sigma_ij, k=min(np.shape(Sigma_ij))-1)
    # cnt = 0
    # for i in s:
    #     if abs(i) > 1e-10:
    #         cnt += 1

    # print('cnt=', cnt)
    # print(Sigma_ij, estimate_rank(aslinearoperator(Sigma_ij), eps=1e-100))
    # print(Sigma_ij, estimate_rank(Sigma_ij.toarray(), eps=1e-100))
    # rg = estimate_rank(Sigma_ij.toarray(), eps=1.0e-20)
    # rg1 = np.linalg.matrix_rank(mat)
    # print('rank=', rg, rg1)
    return np.shape(Sigma_ij)[1] - np.linalg.matrix_rank(Stigma_ij.data)
    # return np.shape(mat)[1] - rg1
    # return np.shape(Sigma_ij)[0] - np.linalg.matrix_rank(Sigma_ij)

# def get_system(n_levels, n_atoms):
#     Sigma_ij = None
#     Sigma_ij_t = None

#     DIM = math.pow(n_levels, n_atoms)
#     # print(DIM)
#     DIM = int(DIM)

#     ab = to_n(DIM-1, n_levels)

#     for i in range(0, n_levels):
#         for j in range(0, i):
#             # print('σ(', i, ',', j, '):', sep='')

#             s_ij = None
#             s_ij_t = None

#             for i_atom in range(1, n_atoms+1):
#                 # -----------------------------------------------------------------------------------------
#                 s = op.Sigma(i_=i, j_=j, num=i_atom,
#                              n_atoms=n_atoms, n_levels=n_levels)
#                 st = op.SigmaT(i_=i, j_=j, num=i_atom,
#                                n_atoms=n_atoms, n_levels=n_levels)
#                 # st = np.transpose(copy.copy(s))

#                 if s_ij is None:
#                     s_ij = s
#                     s_ij_t = st
#                 else:
#                     s_ij += s

#                     s_ij_t += st
#                 # -----------------------------------------------------------------------------------------

#             if Sigma_ij is None:
#                 Sigma_ij = s_ij
#                 Sigma_ij_t = s_ij_t
#             else:
#                 Sigma_ij = np.concatenate((Sigma_ij, s_ij), axis=0)
#                 Sigma_ij_t = np.concatenate((Sigma_ij_t, s_ij_t), axis=0)
#                 ab = np.concatenate((ab, copy.copy(ab)), axis=0)

#     # for i in ab:
#         # print(i)

#     Sigma_ij = np.concatenate((Sigma_ij, Sigma_ij_t), axis=0)
#     ab = np.concatenate((ab, copy.copy(ab)), axis=0)

#     m_, n_ = np.shape(Sigma_ij)

#     Stigma_ij = Matrix(m=m_, n=n_, dtype=int)
#     Stigma_ij.data = Sigma_ij
#     # for i in Stigma_ij.data:
#     # print(''.join([str(int(t)) for t in i]))
#     print(Stigma_ij.m, np.linalg.matrix_rank(Stigma_ij.data), Stigma_ij.n)
#     return Stigma_ij.n - np.linalg.matrix_rank(Stigma_ij.data)
#     # exit(0)
#     Stigma_ij.gray = ab
#     Stigma_ij.init_gray = copy.copy(ab)

#     # for i in Stigma_ij.data:
#     # print(i)
#     print()
#     # print(Stigma_ij.m, Stigma_ij.n)

#     # print(Stigma_ij.m)
#     # exit(0)
#     Stigma_ij.steps()
#     # Stigma_ij.remove_empty_cols()

#     Stigma_ij_short = Matrix(m=Stigma_ij.m, n=Stigma_ij.n, dtype=np.complex128)
#     Stigma_ij_short.data = Stigma_ij.data
#     # print('Stigma_ij_short')
#     # Stigma_ij_short.print()
#     k = 0
#     cnt = 0
#     for i in range(Stigma_ij.m - 1, -1, -1):
#         not_null = 0

#         for t in Stigma_ij.data[i]:
#             if t == 1:
#                 not_null += 1

#         if not_null == 1:
#             cnt += 1
#             # print('k=', k)
#             Stigma_ij_short.remove_row(i)
#             Stigma_ij_short.m -= 1
#             # Stigma_ij_short.print()

#     dim3 = Stigma_ij.n - cnt

#     return Stigma_ij, Stigma_ij_short, dim3, cnt
