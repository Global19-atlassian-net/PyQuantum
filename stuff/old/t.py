from PyQuantum.TC.AtomicBase import *
import numpy as np
import itertools


class Base:
    def __init__(self, capacity, atomic_base):
        self.base = []

        for ph in range(capacity):
            for at in atomic_base.base:
                if ph + at[1] <= capacity:
                    self.base.append([ph, at[0]])

    def print(self):
        for i in self.base:
            print(i)


class AtomicBasis:
    def __init__(self, count, level=2):
        self.basis = itertools.product(range(level), repeat=count)

        self.basis = [list(i) for i in list(self.basis)]

        self.get_energy()

    def get_energy(self):
        self.base = []

        for i in self.basis:
            self.base.append([i, np.sum(i)])

    def print(self):
        for i in self.base:
            print(i)


at = AtomicBasis(count=10, level=3)

base = Base(10, at)
# base.print()
