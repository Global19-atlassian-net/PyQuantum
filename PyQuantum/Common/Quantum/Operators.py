from numpy import matrix, complex128
from math import sqrt


def sigma_x():
    return matrix([[0, 1], [1, 0]], dtype=complex128)


def sigma_y():
    return matrix([[0, complex(0, -1)], [complex(0, 1), 0]], dtype=complex128)


def sigma_z():
    return matrix([[1, 0], [0, -1]], dtype=complex128)


def Hadamard():
    return 1.0 / sqrt(2) * matrix([[1, 1], [1, -1]], dtype=complex128)
