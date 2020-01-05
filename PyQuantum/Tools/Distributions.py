import numpy as np


def Expectation(P, X):
    E = 0

    for i in range(len(P)):
        E += P[i] * X[i]

    return E, E / np.sum(P)


def Variance(P, X, M):
    D = 0

    for i in range(len(P)):
        D += P[i] * (X[i] - M) ** 2

    return D
    # P = np.array(P)
    # X = np.array(X)
    # return Expectation((P-Expectation(P, X))**2, X)


def GeometricDistribution(P, X):
    P_geom = []
    X_geom = []

    q = 1

    for i in range(len(P)):
        P_geom.append(P[i] * q)
        X_geom.append(X[i])

        q *= 1 - P[i]

    return P_geom, X_geom
