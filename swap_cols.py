import numpy as np


def swap_rows(matrix, i, j):
    matrix[i], matrix[j] = matrix[j], matrix[i]

    return


def swap_cols(matrix, j1, j2):
    for i in range(len(matrix)):
        matrix[i][j1], matrix[i][j2] = matrix[i][j2], matrix[i][j1]

    return


def steps(matrix, m, n):
    I = 0
    J = 0

    while I < m and J < n:
        found = False

        for i1 in range(I, m):
            if matrix[i1][J] != 0:
                swap_rows(matrix, i1, I)

                found = True
                break

        if not found:
            J += 1
            continue

        k = matrix[I][J]
        for j1 in range(n):
            matrix[I][j1] /= k

        for i1 in range(m):
            if i1 != I:
                for j1 in range(n):
                    matrix[i1][j1] -= matrix[I][j1] * matrix[i1][j1]

        I += 1
        J += 1

        if I == m or J == n:
            return


matrix = []

m = 3
n = 5

for i in range(m):
    matrix.append([0] * n)


for i in range(m):
    for j in range(n):
        matrix[i][j] = 10 * i + j

matrix[2][0] = 0
matrix[2][1] = 0
matrix[2][2] = 0


for i in matrix:
    print(i)
print()
# exit(0)
# swap_cols(matrix, 0, 1)

steps(matrix, m, n)

for i in matrix:
    print(i)
