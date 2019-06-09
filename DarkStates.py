import PyQuantum.DarkState.operators as op
import PyQuantum.DarkState.qudit as qudit
from PyQuantum.DarkState.D3 import *
from PyQuantum.DarkState.config import *
from PyQuantum.DarkState.Permutations import *
from PyQuantum.Common.Matrix import *
import copy
import math
import DarkSystemSparse as DS

from scipy.sparse import csc_matrix, csr_matrix, linalg as sla

# A = csr_matrix([
#     [0, 1, 1, 0],
#     [0, 0, 0, 1],
#     [0, 0, 0, 1],
#     [0, 0, 0, 0.]
# ])

# u, s, v = np.linalg.svd(A.todense())
# rank = np.sum(s > 1e-10)
# print(rank)

# lu = sla.splu(A)

# print(lu.L.A)
# print(lu.U.A)
# exit(0)

# dim = DS.get_system2(n_levels, n_atoms)

# print('dim =', dim)

# exit(0)


def C_n_k(n, k):
    for n_ in range(0, n+1):
        if n_ == 0:
            c = [1]
        elif n_ == 1:
            c = [1, 1]
        else:
            d = [1] + [(c[i]+c[i+1]) for i in range(len(c)-1)] + [1]

            c = d

        # print(n_, c)

    return c[k]


# for n in range(2, 9, 2):
    # print("n =", n, ":", C_n_k(n, n//2)-C_n_k(n, n//2-1))

for n in range(2, 65, 2):
    print("n =", n, ":", C_n_k(n, n//2)-C_n_k(n-1, n//2))

for n in range(3, 19, 3):
    print("n =", n, ":", C_n_k(n, n//3) - C_n_k(n-1, n//3))
    # print("n =", n, ":", C_n_k(n, n//3)-C_n_k(n, n//3-1))
# print('c', C_n_k(n, 2) / 2)
exit(0)
# ab = np.concatenate((ab, copy.copy(arr)), axis=0)

# print(len(ab))
# for i in ab:
# print(i)
# exit(0)
# print(DIM, math.log2(DIM))
# a = [int(x) for x in bin(DIM)[2:]]
# print(a)

# gray = []
# bitsize = math.ceil(math.log2(DIM))
# for t in range(3):
#     for i in range(DIM):
#         gray.append(format(i, "0"+str(bitsize)+"b"))
# gray.append(format(i, "08b"+str(6)+"b"))

# for i in gray:
#     print(i)
# print(len(gray))
# exit(0)
# -------------------------------------------------------------------------------------------------

print(cnt)
print(n_atoms)
# print('must=', C_n_k(n_atoms, n_atoms//2)-C_n_k(n_atoms, n_atoms//2-1))
exit(0)
# matrix, matrix_short, dim3, cnt = DS.get_system(n_levels, n_atoms)
# gray = matrix.init_gray
# print('matrix')
# matrix.print()

# # 02-11+20

matrix.print()
print('matrix_short')
# matrix_short.remove_empty_cols()
for i in matrix_short.data:
    print(''.join([str(int(t)) for t in i]))

# for i in gray:
# print(i)


def build_tensor(row, gray):
    s = ''
    # print(row)
    for k, v in enumerate(row):
        if v != 0:
            # print(k)
            s += '|' + ''.join([str(t)
                                for t in gray[k]]) + '>'
    return s


cnt = matrix_short.m
for i in range(matrix_short.m):
    row = matrix_short.data[i]
    print(build_tensor(row, gray))
# # print(i, j, '|', ab[j], '>')

# # print(dim3, cnt)
print('cnt =', cnt, 'diff = ', matrix_short.n - cnt)
print('must=', C_n_k(n_atoms, n_atoms//2)-C_n_k(n_atoms, n_atoms//2-1))

exit(0)
# print('-'*100)
# exit(0)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
# lvl = list(itertools.combinations(range(0, n_atoms//2), n_atoms//2))
# lvl = list(itertools.combinations(range(0, n_levels), n_atoms//2))

n = 2
lvl = list(itertools.combinations(
    range(0, n), n))

# lvl = list(itertools.combinations(
#     range(0, n_levels), n_atoms//2))


# lvl = list(itertools.combinations_with_replacement(
#     range(0, n_levels), n_atoms//2))

# lvl = list(itertools.combinations(range(0, n_levels), 3))
# lvl = list(itertools.combinations(range(0, n_levels), 3))
sub = "₀₁₂₃₄₅₆₇₈₉"

# print('lvl=',)
# for p in lvl:
#     print(p)
# exit(0)

# print(123)

# for p1 in lvl:
#     for p2 in lvl:
#         print(p1, p2)
# print()
# exit(0)
cnt2 = 0

for p1 in copy.copy(lvl):
    l1 = list(p1)

    for p2 in copy.copy(lvl):
        l2 = list(p2)

        for p3 in copy.copy(lvl):
            l3 = list(p3)

            print(cnt2, ' ', end='')
            print('(', end='')
            print('|', ''.join([str(i) for i in l1]), '⟩', sep='', end='')
            print(' - |', ''.join([str(i)
                                   for i in l1[::-1]]), '⟩', sep='', end='')
            print(')', end='')
            # -------------------------------------------------------------------------------------
            print(' x ', end='')
            # -------------------------------------------------------------------------------------
            print('(', end='')
            # print(l2)
            print('|', ''.join([str(i) for i in l2]), '⟩', sep='', end='')
            print(' - |', ''.join([str(i)
                                   for i in l2[::-1]]), '⟩', sep='', end='')
            print(')', end='')
            # -------------------------------------------------------------------------------------
            print(' x ', end='')
            # -------------------------------------------------------------------------------------
            print('(', end='')
            print('|', ''.join([str(i) for i in l2]), '⟩', sep='', end='')
            print(' - |', ''.join([str(i)
                                   for i in l2[::-1]]), '⟩', sep='', end='')
            print(')')
            # -------------------------------------------------------------------------------------
            cnt2 += 1
    # print(p1)
    # for p2 in lvl:
    # for k1, t1 in enumerate(p1):
    #     # for k2, t2 in enumerate(p2):
    #     print('|', t1, '>', sub[k1], sep='', end='')
    #     print()
    # print(p1, p2)
print('cnt2 =', cnt2)
exit(0)

permutations = Permutations(n_levels)

# for p in permutations:
# print(p)

# x = list(itertools.combinations('ABCD', 2))

x3 = list(itertools.permutations(range(0, n_atoms), n_atoms//2))
# x = list(itertools.combinations_with_replacement('ABCD', 2))
# for i in x3:
# print(i)


# -----------------------------------------------------------------------------------------
States = []

base3 = itertools.permutations(range(0, n_atoms), n_atoms//2)
# xxx = list(itertools.combinations_with_replacement('ABCD', 2))
for i in x3:
    print(i)

# print('base2:', base3)
# print(set(permutations))
# exit(0)


def diff(perm, x):
    other = set()
    # other = []

    for v in perm:
        if v != x:
            other.add(v)
            # other.append(v)

    return other


base3 = frozenset(base3)


# for i in base3:
#     print(i)

S = list(itertools.combinations_with_replacement(
    ''.join([str(i) for i in range(n_levels)]), n_atoms//2))

xx = list(itertools.combinations(
    ''.join([str(i) for i in range(n_atoms)]), n_atoms//2))


# xx = list(itertools.combinations(
#     ''.join([str(i) for i in range(n_atoms)]), n_atoms//2))
# xx = [set(i) for i in xx]
# for i in S:
#     print(i)
# for i in xx:
#     print(i)
# exit(0)


# cnt = 0


# for atoms_1 in xx:
#     for atoms_2 in diff(xx, atoms_1):
#         for s1 in S:
#             print('s1:')
#             print(s1)
#             print('D1:')
#             d1 = DarkState(s1, n_levels=n_levels, base=list(s1))
#             d1.print()

#             for s2 in S:
#                 if len(set(atoms_1).intersection(atoms_2)) != 0:
#                     continue

#                 if set(atoms_1) == set(atoms_2):
#                     continue

#                 # print(s1)

#                 print('\tD2:', end='')
#                 d2 = DarkState(s2, n_levels=n_levels, base=list(s1))
#                 d2.print()
#                 # for b1 in s1:
#                 #     for b2 in s2:
#                 #         for a1 in atoms_1:
#                 #             for a2 in atoms_2:
#                 #                 s_ = ''
#                 #                 s_ += '|'+b1+'⟩' + \
#                 #                     sub[int(a1)] + 'x |' + b2 + \
#                 #                     '⟩' + sub[int(a2)]

#                 #                 print(s_)
#                 # print(s1, '_', atoms_1, ' ', s2, '_', atoms_2, sep='')
#             # print(atoms_1, atoms_2)

#             cnt += 1
#         exit(0)
# print('cnt =', cnt)

# for p in x3:
# print(p)
# print(p, set(range(1, n_atoms+1)),
# set(range(1, n_atoms+1))-set(p))
# d3 = DarkState(p, n_levels=n_levels, base=list(b))
# d6 = DarkState(p, n_levels=n_levels,
# base=range(n_atoms//2+1, n_atoms+1))
# d6 = DarkState(set(range(1, n_atoms+1)) -
# set(p), n_levels=n_levels)
# print('base')
# for i in d6.base:
#     print(i)
# exit(0)
# print('\t\t', end='')
# d = d3.tensor(d6)
# d3.print(style='dirac')
# print('\t\t', end='')
# d6.print(style='dirac')

# States.append(d)
# D = np.sum(States)

# print("\nD:")
# print(D.state)

# print('x3 =', len(x3))
# print('perm =', len(permutations))

# dim_1 = np.shape(D.state)[0] - np.ndim(D.state)
# dim_1 = np.linalg.matrix_rank(D.state)
# print(np.shape(D.state)[0])
# print('dim_1 = ', dim_1, sep='')
# for b in D.base:
# print(b)
# print('dim = ', np.shape(D.state), D.base)
# -----------------------------------------------------------------------------------------

# print('-'*100)
# '-'*100)
# -'*100)
