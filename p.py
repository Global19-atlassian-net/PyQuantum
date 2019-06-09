import itertools
import copy

n_atoms = 4

base3 = itertools.permutations(range(0, n_atoms), n_atoms//2)
base3 = frozenset(base3)

for i in base3:
    print(i)


def diff(perm, x):
    other = set()
    # other = []

    for v in perm:
        if v != x:
            other.add(v)
            # other.append(v)

    return other

# print()


for i in base3:
    print(i, diff(base3, i))

# # base33 = itertools.permutations(range(0, n_atoms), n_atoms//2)
# # base33 = set(base33)
# base33 = copy.deepcopy(base3)
# # d = set()
# for i in base3:
#     # s = set(i)
#     # print(type(base3))
#     b = copy.copy(base33)
#     ii = copy.copy((i))
#     d = set(b).difference(set(ii))
#     # d = set(itertools.permutations(
#     # range(0, n_atoms), n_atoms//2))-set((i))
#     print(i, d)
#     # print('base:', set(base3))
# # print(set(tuple(i)))

# print(5)
# # base3 = list(itertools.permutations(range(0, n_atoms), n_atoms//2))
# x = list(itertools.combinations_with_replacement('ABCD', 2))
# print(base3)

# # for i in base3:
# # print(i)
# d = list(base3)
# d = set(d)

# print(d)
# s = (0, 1)
# print(s)
# print(d - s)

# print(5)

# for i in d:
#     a = set(base3) - set(i)
#     print(a)
# print(2, set(i), i)
# print(set(base3)-set(i), i)
# print(i, base3 - i)
