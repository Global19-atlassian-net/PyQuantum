# from PyQuantum.TC.FullBase import *
from PyQuantum.TC.AtomicBase import *


class Base:
    def __init__(self, capacity, atomic_base):
        self.base = []

        for ph in range(capacity+1):
            for at in atomic_base.base:
                if ph + at[1] == capacity:
                    self.base.append([[ph, at[0]], capacity])

    def print(self):
        for i in self.base:
            print(i)


class LindbladBase:
    def __init__(self, capacity):
        self.base = []

        a = AtomicBasis(count=capacity*2)

        for ph in range(capacity+1):
            d = Base(capacity=ph, atomic_base=a)
            self.base += d.base
            # self.base.extend(d)

        # for i in self.base:
            # print(i)


# a = AtomicBasis(count=5)
# a.print()

# b = Base(capacity=0, atomic_base=a)

# b.print()
n = 10

c = LindbladBase(capacity=n)
print(len(c.base))
# b.print()
# import itertools
# import numpy as np


# def decart(*arrays, limit=2):
#     res = np.array(list(itertools.product(*arrays)))

#     for i in range(len(res)-1, -1, -1):
#         if np.sum(res[i]) > limit:
#             res = np.delete(res, i, axis=0)

#     return res


# # def decart2(*arrays):
# #     res = arrays[0]

# #     for i in range(1, len(arrays)):
# #         res = itertools.dotproduct(res, arrays[i])
# #         # res = np.array(list(itertools.product(list(res), arrays[i])))
# #         print(res)
# #     return res

# class AtomicBasis:
#     def __init__(self, count):
#         self.basis = itertools.product(range(2), repeat=count)
#         self.basis = list(self.basis)

#     def get_energy(self):
#         self.base = []

#         for i in self.basis:
#             self.base.append([i, np.sum(i)])
#             # print(np.sum(i))

#     def print(self):
#         for i in self.base:
#             print(i)


# capacity = 5

# a = AtomicBasis(count=capacity)


# a.get_energy()
# # a.print()


# class Base:
#     def __init__(self, capacity, atomic_base):
#         self.base = []

#         for ph in range(capacity):
#             for at in atomic_base.base:
#                 if ph + at[1] <= capacity:
#                     self.base.append([ph, at[0]])

#     def print(self):
#         for i in self.base:
#             print(i)


# b = Base(capacity=capacity, atomic_base=a)
# # print(a)
# b.print()
# # print(len(b.base))
# print("y")
# exit(0)

# ph = [0, 1, 15]
# at_1 = [0, 1]
# at_2 = [0, 1]
# args = [at_2]*14
# # c = decart(ph, *args, limit=15)

# c = itertools.product(range(2), repeat=14)
# print(len(list(c)))
# exit(0)
# d = itertools.product(range(15), c)
# d = list(d)

# for i in range(len(d)-1, -1, -1):
#     lvl = d[i][0] + np.sum(d[i][1])
#     # print(lvl)

#     if lvl > 15:
#         d.remove(d[i])

# for i in d:
#     print(i)
# # print(i, np.sum(i, keepdims=False))
# exit(0)
# # print(list(d))
# # c = decart2(at_1, at_2, at_1)

# print(c)
