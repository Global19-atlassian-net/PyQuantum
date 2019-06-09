from scipy import sparse
import numpy as np
import scipy


def sigma(n_levels, i, j):
    sigma = np.zeros([n_levels, n_levels])

    sigma[j][i] = 1

    return sigma


def sigma_cross(n_levels, i, j):
    return np.transpose(sigma(n_levels, i, j))


# def Sigma(i_, j_, num, n_atoms, n_levels):
#     # i_ -> j_
#     # num: 1 - first atom
#     I_at = np.identity(n_levels)

#     sigma_i_j_num = None

#     if num == 1:
#         sigma_i_j_num = sigma(n_levels, i_, j_)
#         # print(sigma_i_j_num)
#         for i in range(n_atoms-1):
#             sigma_i_j_num = np.kron(sigma_i_j_num, I_at)
#             # print(I_at)
#     elif num == n_atoms:
#         sigma_i_j_num = I_at
#         # print(sigma_i_j_num)

#         for i in range(n_atoms-2):
#             sigma_i_j_num = np.kron(sigma_i_j_num, I_at)
#             # print(I_at)
#         sigma_i_j_num = np.kron(sigma_i_j_num, sigma(n_levels, i_, j_))
#         # print(sigma(n_levels, i_, j_))
#     else:
#         sigma_i_j_num = I_at
#         # print(sigma_i_j_num)
#         # print(num-1)
#         for i in range(num-2):
#             sigma_i_j_num = np.kron(sigma_i_j_num, I_at)
#             # print(I_at)

#         sigma_i_j_num = np.kron(sigma_i_j_num, sigma(n_levels, i_, j_))
#         # print(sigma(n_levels, i_, j_))

#         for i in range(num, n_atoms):
#             sigma_i_j_num = np.kron(sigma_i_j_num, I_at)
#             # print(I_at)
#     return sigma_i_j_num


# def SigmaT(i_, j_, num, n_atoms, n_levels):
#     # i_ -> j_
#     # num: 1 - first atom
#     I_at = np.identity(n_levels)

#     sigma_i_j_num = None

#     if num == 1:
#         sigma_i_j_num = sigma_cross(n_levels, i_, j_)
#         # print(sigma_i_j_num)
#         for i in range(n_atoms-1):
#             sigma_i_j_num = np.kron(sigma_i_j_num, I_at)
#             # print(I_at)
#     elif num == n_atoms:
#         sigma_i_j_num = I_at
#         # print(sigma_i_j_num)

#         for i in range(n_atoms-2):
#             sigma_i_j_num = np.kron(sigma_i_j_num, I_at)
#             # print(I_at)
#         sigma_i_j_num = np.kron(sigma_i_j_num, sigma_cross(n_levels, i_, j_))
#         # print(sigma(n_levels, i_, j_))
#     else:
#         sigma_i_j_num = I_at
#         # print(sigma_i_j_num)
#         # print(num-1)
#         for i in range(num-2):
#             sigma_i_j_num = np.kron(sigma_i_j_num, I_at)
#             # print(I_at)

#         sigma_i_j_num = np.kron(sigma_i_j_num, sigma_cross(n_levels, i_, j_))
#         # print(sigma(n_levels, i_, j_))

#         for i in range(num, n_atoms):
#             sigma_i_j_num = np.kron(sigma_i_j_num, I_at)
#             # print(I_at)
#     return sigma_i_j_num


# def SigmaCross(i_, j_, num):
#     I_at = np.identity(n_levels)

#     sigma_i_j_num = None

#     if num == 1:
#         sigma_i_j_num = op.sigma_cross(n_levels, i_, j_)

#         for i in range(n_atoms-1):
#             sigma_i_j_num = np.kron(sigma_i_j_num, I_at)
#     elif num == n_atoms:
#         sigma_i_j_num = I_at

#         for i in range(n_atoms-2):
#             sigma_i_j_num = np.kron(sigma_i_j_num, I_at)

#         sigma_i_j_num = np.kron(
#             sigma_i_j_num, op.sigma_cross(n_levels, i_, j_))
#     else:
#         sigma_i_j_num = I_at

#         for i in range(num-1):
#             sigma_i_j_num = np.kron(sigma_i_j_num, I_at)

#         sigma_i_j_num = np.kron(
#             sigma_i_j_num, op.sigma_cross(n_levels, i_, j_))

#         for i in range(num+1, n_atoms):
#             sigma_i_j_num = np.kron(sigma_i_j_num, I_at)

#     return sigma_i_j_num
# def Sigma(n_atoms, n_levels=2):
#     s = None
#     # s = np.zeros([np.shape(s)[0], np.shape(s)[1]])

#     for i in range(1, n_atoms+1):
#         for i1 in range(1, 2):
#             # for i1 in range(1, n_levels):
#             for i2 in range(i1):
#                 print('i = ', i, ' (', i1, ',', i2, ')', sep='')
#                 s_ = Sigma(i1, i2, i)

#                 if s in None:
#                     s = s_
#                 else:
#                     s += s_
#                 print(s)
#                 print()

#     return s


# sigma_1_0 = op.sigma(3, 1, 0)
# sigma_2_0 = op.sigma(3, 2, 0)
# sigma_2_1 = op.sigma(3, 2, 1)

# print(sigma_1_0)
# print(sigma_2_0)
# print(sigma_2_1)

# exit(0)


def Sigma2(i_, j_, num, n_atoms, n_levels):
    # i_ -> j_
    # num: 1 - first atom
    I_at = scipy.sparse.identity(n_levels, dtype=float)

    sigma_i_j_num = None

    if num == 1:
        sigma_i_j_num = sigma(n_levels, i_, j_)

        for i in range(n_atoms-1):
            sigma_i_j_num = sparse.kron(sigma_i_j_num, I_at)

    elif num == n_atoms:
        sigma_i_j_num = I_at

        for i in range(n_atoms-2):
            sigma_i_j_num = sparse.kron(sigma_i_j_num, I_at)

        sigma_i_j_num = sparse.kron(sigma_i_j_num, sigma(n_levels, i_, j_))
    else:
        sigma_i_j_num = I_at

        for i in range(num-2):
            sigma_i_j_num = sparse.kron(sigma_i_j_num, I_at)

        sigma_i_j_num = sparse.kron(sigma_i_j_num, sigma(n_levels, i_, j_))

        for i in range(num, n_atoms):
            sigma_i_j_num = sparse.kron(sigma_i_j_num, I_at)

    return sigma_i_j_num


def Sigma2T(i_, j_, num, n_atoms, n_levels):
    # i_ -> j_
    # num: 1 - first atom
    I_at = scipy.sparse.identity(n_levels, dtype=float)

    sigma_i_j_num = None

    if num == 1:
        sigma_i_j_num = sigma_cross(n_levels, i_, j_)

        for i in range(n_atoms-1):
            sigma_i_j_num = sparse.kron(sigma_i_j_num, I_at)
    elif num == n_atoms:
        sigma_i_j_num = I_at

        for i in range(n_atoms-2):
            sigma_i_j_num = sparse.kron(sigma_i_j_num, I_at)

        sigma_i_j_num = sparse.kron(
            sigma_i_j_num, sigma_cross(n_levels, i_, j_))
    else:
        sigma_i_j_num = I_at

        for i in range(num-2):
            sigma_i_j_num = sparse.kron(sigma_i_j_num, I_at)

        sigma_i_j_num = sparse.kron(
            sigma_i_j_num, sigma_cross(n_levels, i_, j_))

        for i in range(num, n_atoms):
            sigma_i_j_num = sparse.kron(sigma_i_j_num, I_at)

    return sigma_i_j_num
