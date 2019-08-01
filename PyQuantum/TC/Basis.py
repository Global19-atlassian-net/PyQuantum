import itertools
import numpy as np


class Basis:
    def __init__(self, capacity, n_atoms, n_levels):
        self.atomic_basis = itertools.product(range(n_levels), repeat=n_atoms)
        self.atomic_basis = list(map(list, self.atomic_basis))

        self.ph_basis = np.arange(capacity+1)

        self.basis = []

        for ph_state in self.ph_basis:
            for at_state in self.atomic_basis:
                self.basis.append([ph_state, at_state])
