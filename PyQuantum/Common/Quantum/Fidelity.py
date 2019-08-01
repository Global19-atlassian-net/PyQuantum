# -------------------------------------------------------------------------------------------------
# scientific
import numpy as np
import scipy.sparse.linalg as lg
# -------------------------------------------------------------------------------------------------
from PyQuantum.Common.Matrix import *

# -------------------------------------------------------------------------------------------------


# def Fidelity(ro_sqrt, sigma):
#     fid_matrix = (ro_sqrt.dot(sigma.data).dot(ro_sqrt)).sqrt()
#     # fid_matrix = lg.fractional_matrix_power(
#     #     ro_sqrt.dot(sigma).dot(ro_sqrt), 0.5)
#     return np.sum(np.abs(fid_matrix.diagonal()))
# -------------------------------------------------------------------------------------------------


def Fidelity_full(w_1, w_2):
    return lg.norm(w_1.data.getH().dot(w_2.data))
    # w_1.data = w_1.data.power(0.5)
    # w_1.print()
    # exit(0)
    # w_1_sqrt = w_1.data.power(0.5)
    # # w_1_sqrt = w_1.data.sqrt()

    # fid_matrix = (w_1_sqrt.dot(w_2.data).dot(w_1_sqrt)).power(0.5)

    # return abs(np.sum(fid_matrix.diagonal()) ** 2)
    # return np.sum(np.abs(fid_matrix.diagonal())) ** 2
