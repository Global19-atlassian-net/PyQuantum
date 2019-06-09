from PyQuantum.Common.SparseMatrix.SparseMatrix import *
from numpy.linalg import matrix_rank
import numpy as np

MAX_VALUE = 100

M_MIN = 2
M_MAX = 5

N_MIN = 2
N_MAX = 5

N_TESTS = 100

print('-'*100)

for m in range(M_MIN, M_MAX+1):
    print('m =', m)

    for n in range(m, N_MAX+1):
        print('\tn =', n, '\n')
    for k in range(N_TESTS):
        m_1 = []

        for i_ in range(m):
            m_1.append(np.random.randint(MAX_VALUE+1, size=n))

        # ----------------------------------------------------
        # print()
        # for line in m_1:
        #     print(line)
        # ----------------------------------------------------
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
        else:
            print('\ttest 0..', k, ': ok', sep='', end='')

            if k != N_TESTS-1:
                print('\r', end='')
            else:
                print()
            # print('OK')
            # print('*'*100)
    print('-'*100)
