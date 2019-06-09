# from SparseMatrix import *
from PyQuantum.Common.SparseMatrix.SparseMatrix import *
from PyQuantum.Common.Assert import *


# -------------------------------------------------------------------------------------------------
def sigma(i, j, n_levels):
    Assert(i >= 0, "i < 0", cf())
    Assert(j >= 0, "j < 0", cf())
    Assert(n_levels > 0, "n_levels <= 0", cf())

    sigma = SparseMatrix(m=n_levels, n=n_levels, orient='row')

    sigma.add((j, i), 1)

    return sigma
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
def identity(n):
    Assert(n > 0, "n <= 0", cf())

    I = SparseMatrix(orient='row')

    for i in range(n):
        I.add((i, i), 1)

    return I
# -------------------------------------------------------------------------------------------------


def kron(A, B):
    C = SparseMatrix(m=A.m*B.m, n=A.n*B.n, orient='row')

    # for k, v in A.row.items():
    #     print(k, v)
    # print()
    # for k, v in B.row.items():
    #     print(k, v)
    # print()

    for k_i, v_i in A.row.items():
        for k_j, v_j in B.row.items():
            for ki_a, vi_a in enumerate(A.row[k_i]['ind']):
                for kj_a, vj_a in enumerate(B.row[k_j]['ind']):
                    val1 = v_i['items'][ki_a]
                    val2 = v_j['items'][kj_a]

                    # print(vi_a, vj_a)

                    # print('C[', k_i, '*', B.m, '+', kj_a, ',',
                    #       vi_a, '*', B.n, '+', vj_a, '] = ', sep='', end='')
                    # print('C[', k_i*B.m+kj_a, ',', vi_a*B.n+vj_a, ']', sep='')

                    C.add((k_i*B.m+k_j, vi_a*B.n+vj_a), val1*val2)

                    # print(C.m, C.n)

    return C


def sigma_(n_levels, i, j):
    sigma = SparseMatrix(m=n_levels, n=n_levels)

    sigma.add((j, i), 1)

    return sigma


def sigma_cross_(n_levels, i, j):
    sigma = SparseMatrix(m=n_levels, n=n_levels)

    sigma.add((i, j), 1)

    return sigma
    # return np.transpose(sigma(n_levels, i, j))

# -------------------------------------------------------------------------------------------------


def Sigma2(i_, j_, num, n_atoms, n_levels):
    # i_ -> j_
    # num: 1 - first atom
    I_at = identity(n_levels)

    sigma_i_j_num = None

    if num == 1:
        sigma_i_j_num = sigma_(n_levels, i_, j_)

        for i in range(n_atoms-1):
            sigma_i_j_num = kron(sigma_i_j_num, I_at)

    elif num == n_atoms:
        sigma_i_j_num = I_at

        for i in range(n_atoms-2):
            sigma_i_j_num = kron(sigma_i_j_num, I_at)

        sigma_i_j_num = kron(sigma_i_j_num, sigma_(n_levels, i_, j_))
    else:
        sigma_i_j_num = I_at

        for i in range(num-2):
            sigma_i_j_num = kron(sigma_i_j_num, I_at)

        sigma_i_j_num = kron(sigma_i_j_num, sigma_(n_levels, i_, j_))

        for i in range(num, n_atoms):
            sigma_i_j_num = kron(sigma_i_j_num, I_at)

    return sigma_i_j_num


def Sigma2T(i_, j_, num, n_atoms, n_levels):
    # i_ -> j_
    # num: 1 - first atom
    I_at = identity(n_levels)

    sigma_i_j_num = None

    if num == 1:
        sigma_i_j_num = sigma_cross_(n_levels, i_, j_)

        for i in range(n_atoms-1):
            sigma_i_j_num = kron(sigma_i_j_num, I_at)

    elif num == n_atoms:
        sigma_i_j_num = I_at

        for i in range(n_atoms-2):
            sigma_i_j_num = kron(sigma_i_j_num, I_at)

        sigma_i_j_num = kron(sigma_i_j_num, sigma_cross_(n_levels, i_, j_))
    else:
        sigma_i_j_num = I_at

        for i in range(num-2):
            sigma_i_j_num = kron(sigma_i_j_num, I_at)

        sigma_i_j_num = kron(sigma_i_j_num, sigma_cross_(n_levels, i_, j_))

        for i in range(num, n_atoms):
            sigma_i_j_num = kron(sigma_i_j_num, I_at)

    return sigma_i_j_num
