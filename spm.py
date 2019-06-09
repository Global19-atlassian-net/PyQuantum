# ****************************************************************************************************
# ----------------------------------------------------------------------------------------------------
# divs = 2612, subs = 96483
# ****************************************************************************************************
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# rg = 153 , n = 243
# dim = 90
# ****************************************************************************************************


# ****************************************************************************************************
# ----------------------------------------------------------------------------------------------------
# divs = 1293, subs = 43280
# ****************************************************************************************************
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# rg = 153 , n = 243
# dim = 90

# real	0m16,206s
# user	0m11,234s
# sys	0m0,504s
# ****************************************************************************************************


from PyQuantum.Common.SparseMatrix.SparseMatrix import *
from PyQuantum.Common.SparseMatrix.operators import *

n_atoms = 2
n_levels = 3

Sigma_ij = None

for i in range(0, n_levels):
    for j in range(0, i):
        s_ij = None
        # s_ij_t = None

        for i_atom in range(1, n_atoms+1):
            # -----------------------------------------------------------------------------------------
            s = Sigma2(i_=i, j_=j, num=i_atom,
                       n_atoms=n_atoms, n_levels=n_levels)
            # st = Sigma2T(i_=i, j_=j, num=i_atom,
            # n_atoms=n_atoms, n_levels=n_levels)
            # st = np.transpose(copy.copy(s))

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
        # print(s_ij)
        # Sigma_ij = vstack((Sigma_ij, s_ij))
        # Sigma_ij = np.concatenate((Sigma_ij, s_ij), axis=0)
        # Sigma_ij_t = np.concatenate((Sigma_ij_t, s_ij_t), axis=0)
        # Sigma_ij_t = vstack((Sigma_ij_t, s_ij_t))
        # ab = np.concatenate((ab, copy.copy(ab)), axis=0)
        # ab = hstack((ab, copy.copy(ab)))
        print('*' * 100)
        # Sigma_ij.add((0, 0), 5)
        # Sigma_ij.Print()
        # Sigma_ij.print_rows()
        # print(123)
        # exit(0)
        # Sigma_ij.Print(mode='full')
        print('-' * 100)
        Sigma_ij.Print(mode="full")
        r, m, I = Sigma_ij.rank()
        # Sigma_ij.Print(mode='non-zero')
        print('*' * 100)
        # Sigma_ij.Print(mode='full')
        print('-' * 100)
        # Sigma_ij.info()
        print('-' * 100)
        print('rg =', r, ', n =', Sigma_ij.n)

        print('dim =', Sigma_ij.n - r)
        # print(m.m, I.m)
        # m.info()
        # I.info()
        # print(len(I.row))
        # m.Print(mode="full")
        # I.Print(mode="full")
        exit(0)

print('*' * 100)
# Sigma_ij_t.to_csv('6_3.csv')
# Sigma_ij.Print(mode='full')
exit(0)


print('-' * 100)
# Sigma_ij_t.Print(mode='full')
print('*' * 100)
# print()

print('*' * 100)
r = Sigma_ij.rank()
# print('rank = ', r, ', dim = ', Sigma_ij.n, sep='')
# Sigma_ij.Print(mode='full')
exit(0)
print('-' * 100)

r = Sigma_ij_t.rank()
print('rank = ', r, ', dim = ', Sigma_ij_t.n, sep='')

# Sigma_ij_t.Print(mode='full')
print('*' * 100)
exit(0)


# for i in ab:
# print(i)
# print(Sigma_ij)
# Sigma_ij = vstack((Sigma_ij, Sigma_ij_t))
# Sigma_ij = np.concatenate((Sigma_ij, Sigma_ij_t), axis=0)
# ab = np.concatenate((ab, copy.copy(ab)), axis=0)
# ab = hstack((ab, copy.copy(ab)))

# m_, n_ = np.shape(Sigma_ij)
# s2.Print(mode='full')

exit(0)

matrix = SparseMatrix()

matrix.add((0, 2), 5)
matrix.add((1, 2), 3)
matrix.add((1, 1), 4)
matrix.add((2, 2), 4)
matrix.add((2, 2), 4)

# matrix.print()
# print()
print('*'*100)
matrix.Print(mode='full')
print('*'*100)

# matrix.remove(1, 2)
# matrix.add((1, 2), 3)
# matrix.remove(1, 2)
# matrix.swap_rows(1, 2)
r = matrix.rank()

print('rank =', r)

print('*'*100)
matrix.Print(mode='full')
print('*'*100)

# matrix.info()
# matrix.empty()
matrix.info()

# I = identity(2)

# I.print(mode='full')
# print()
# I = kron(I, I)

# I.print(mode='full')

# r = matrix.rank()


# print(matrix.m, matrix.n, matrix.count)


# # -------------------------------------------------------------------------------------------------
# def sigma(i, j, n_levels):
#     Assert(i >= 0, "i < 0", cf())
#     Assert(j >= 0, "j < 0", cf())
#     Assert(n_levels > 0, "n_levels <= 0", cf())

#     sigma = SparseMatrix(m=n_levels, n=n_levels, orient='row')

#     sigma.add(j, i, 1)

#     return sigma
# # -------------------------------------------------------------------------------------------------


# # -------------------------------------------------------------------------------------------------
# def identity(n):
#     Assert(n > 0, "n <= 0", cf())

#     I = SparseMatrix(orient='row')

#     for i in range(n):
#         I.add(i, i, 1)

#     return I
# # -------------------------------------------------------------------------------------------------


# def kron(A, B):
#     C = SparseMatrix(m=A.m*B.m, n=A.n*B.n, orient='row')

#     for k, v in A.row.items():
#         print(k, v)
#     print()
#     for k, v in B.row.items():
#         print(k, v)
#     print()

#     for k_i, v_i in A.row.items():
#         for k_j, v_j in B.row.items():
#             for ki_a, vi_a in enumerate(A.row[k_i]['ind']):
#                 for kj_a, vj_a in enumerate(B.row[k_j]['ind']):
#                     val1 = v_i['data'][ki_a]
#                     val2 = v_j['data'][kj_a]

#                     # print(vi_a, vj_a)

#                     # print('C[', k_i, '*', B.m, '+', kj_a, ',',
#                     #       vi_a, '*', B.n, '+', vj_a, '] = ', sep='', end='')
#                     # print('C[', k_i*B.m+kj_a, ',', vi_a*B.n+vj_a, ']', sep='')

#                     C.add(k_i*B.m+k_j, vi_a*B.n+vj_a, val1*val2)

#                     # print(C.m, C.n)

#     return C


# def sigma_(n_levels, i, j):
#     sigma = SparseMatrix(m=n_levels, n=n_levels)

#     sigma.add(j, i, 1)

#     return sigma


# # def sigma_cross(n_levels, i, j):
#     # return np.transpose(sigma(n_levels, i, j))

# # -------------------------------------------------------------------------------------------------


# def Sigma2(i_, j_, num, n_atoms, n_levels):
#     # i_ -> j_
#     # num: 1 - first atom
#     I_at = identity(n_levels)

#     sigma_i_j_num = None

#     if num == 1:
#         sigma_i_j_num = sigma_(n_levels, i_, j_)

#         for i in range(n_atoms-1):
#             sigma_i_j_num = kron(sigma_i_j_num, I_at)

#     elif num == n_atoms:
#         sigma_i_j_num = I_at

#         for i in range(n_atoms-2):
#             sigma_i_j_num = kron(sigma_i_j_num, I_at)

#         sigma_i_j_num = kron(sigma_i_j_num, sigma_(n_levels, i_, j_))
#     else:
#         sigma_i_j_num = I_at

#         for i in range(num-2):
#             sigma_i_j_num = kron(sigma_i_j_num, I_at)

#         sigma_i_j_num = kron(sigma_i_j_num, sigma_(n_levels, i_, j_))

#         for i in range(num, n_atoms):
#             sigma_i_j_num = kron(sigma_i_j_num, I_at)

#     return sigma_i_j_num


# s2 = Sigma2(1, 1, 2, n_atoms=2, n_levels=3)
# s2.print(mode='full')
# exit(0)
# print('-'*100)

# print('sigma10:')
# sigma10 = sigma(1, 0, n_levels=3)
# # sigma11 = sigma(1, 0, n_levels=3)
# # sigma10 -= 10
# # sigma10 / 2
# # sigma10.print()

# sigma10 += identity(3)
# # sigma10 -= sigma10
# sigma10.print(mode='full')
# exit(0)
# # print()
# sigma10.print(mode='full')

# # print('-'*100)

# # print('sigma20:')
# # sigma20 = sigma(2, 0, n_levels=3)
# # sigma20.print()
# # print()
# # sigma20.print(mode='full')

# # print('-'*100)

# # print('sigma21:')
# # sigma21 = sigma(2, 1, n_levels=3)
# # sigma21.print()
# # print()
# # sigma21.print(mode='full')

# # print('-'*100)
# # # -------------------------------------------------------------------------------------------------

# # I = identity(3)
# # I.print()
# # I.print(mode='full')


# # C = kron(I, sigma20)
# # # print('123')
# # # for k, v in C.row.items():
# # # print(k, v)
# # C.print(mode='full')
# # print()
# # C.print()
# # # print('456')
# # exit(0)

# # spm = SparseMatrix(orient='row')
# # spm.add(5, 2, 1)
# # spm.add(5, 1, 3)
# # spm.add(3, 1, -15)

# # for k, v in spm.row.items():
# #     print(k, v)

# # spm.print(mode='full')
# # print()
# # spm.print()

# # spm.sort_rows_by_count()

# # spm + 12

# # spm.to_csv('1.csv')


# s = identity(3)
# # s.divide_row(0, 3)
# # s.mult_row(0, 1)
# # s.add_row(2, -1)
# s.add((0, 0), 35)
# s.info()
# # s.add((0, 1), 15)
# s.Print(mode='full')
# s.info()
# exit(0)
# s2 = Sigma2(i_=1, j_=1, num=2, n_atoms=2, n_levels=3)
# for i in range(1, 5):
