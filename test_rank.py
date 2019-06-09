from PyQuantum.Common.SparseMatrix.SparseMatrix import *
from numpy.linalg import matrix_rank
import numpy as np

m = 3
n = 3

m_1 = [
    [81, 62, 17],
    [59, 58, 28],
    [15, 58,  0],
]

print()
for line in m_1:
    print(line)

rg_1 = matrix_rank(m_1)

m_2 = SparseMatrix()

for i in range(m):
    for j in range(n):
        m_2.add((i, j), m_1[i][j])

rg_2, short, I = m_2.rank()

if rg_1 != rg_2:
        # for line in m_1:
        #     print(line)

    print('rg_1 = ', rg_1, ', rg_2 = ', rg_2, sep='')
    print()
    print('matrix:')
    short.Print(mode='full')
    print()
    print('I:')
    I.Print(mode='full')
    exit(0)
# else:
    # print('\ttest 0..', k, ': ok', sep='', end='')
    # if k != N_TESTS-1:
    #     print('\r', end='')
    # else:
    #     print()
    # print('OK')
    # print('*'*100)
