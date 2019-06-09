import itertools

import numpy as np


def get_ph_base_chain(capacity, cv_chain):
    ph = []

    for cv in cv_chain.cavities:
        ph_base = list(itertools.product(range(capacity+1), repeat=1))
        ph_base = [list(i) for i in ph_base]

        ph.append(ph_base)

    AtomicBase = list(itertools.product(*ph))
    AtomicBase = [list(i) for i in AtomicBase]

    for i in AtomicBase:
        print(i)

    return AtomicBase


def get_at_base_chain(capacity, cv_chain):
    atomic_base_chain = []

    for cv in cv_chain.cavities:
        atomic_base = list(itertools.product(range(2), repeat=capacity))
        atomic_base = [list(i) for i in atomic_base]

        atomic_base_chain.append(atomic_base)

    print(atomic_base_chain)

    AtomicBase = itertools.product(*atomic_base_chain)

    AtomicBase = [list(i) for i in AtomicBase]

    return AtomicBase


def get_full_base(capacity, cv_chain, limit=True):
    BASE = []

    ph_chain = get_ph_base_chain(capacity, cv_chain)
    AtomicBase = get_at_base_chain(capacity, cv_chain)

    for i in range(np.shape(ph_chain)[0]):
        for j in range(np.shape(AtomicBase)[0]):
            state = []

            energy = 0

            for cv in range(0, len(cv_chain.cavities)):
                state.append([ph_chain[i][cv][0], AtomicBase[j][cv]])

                energy += ph_chain[i][cv][0]
                energy += np.sum(AtomicBase[j][cv])

            if limit:
                if energy > capacity:
                    continue

            BASE.append(state)

    for i in BASE:
        print(i)

    return BASE

# from PyQuantum.TCH.AtomicBase import *


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
