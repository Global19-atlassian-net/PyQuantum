# ---------------------------------------------------------------------------------------------------------------------
# system
import itertools
# ---------------------------------------------------------------------------------------------------------------------
# scientific
import numpy as np
# ---------------------------------------------------------------------------------------------------------------------



class Basis:
    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- INIT -------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, capacity, n_atoms, n_levels):
        self.sink_basis = itertools.product(range(2), repeat=2)
        self.sink_basis = list(map(list, self.sink_basis))
        self.atomic_basis = itertools.product(range(n_levels), repeat=n_atoms)
        self.atomic_basis = list(map(list, self.atomic_basis))

        self.basis = []

        if isinstance(capacity, int):
            self.ph_basis = np.arange(capacity+1)
            for ph_state in self.ph_basis:
                for at_state in self.atomic_basis:
                    self.basis.append([ph_state, at_state])
        elif isinstance(capacity, dict):
            self.ph_basis_01 = np.arange(capacity['0_1']+1)
            self.ph_basis_12 = np.arange(capacity['1_2']+1)

            for ph_state_01_ in self.ph_basis_01:
                for ph_state_12_ in self.ph_basis_12:
                    for at_state in self.atomic_basis:
                        for sink_state in self.sink_basis:
                            self.basis.append(
                                [ph_state_01_, ph_state_12_, at_state, sink_state])
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

# =====================================================================================================================
