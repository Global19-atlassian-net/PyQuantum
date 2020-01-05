# -------------------------------------------------------------------------------------------------
# scientific
import numpy as np
import copy
# -------------------------------------------------------------------------------------------------
# Common
from PyQuantum.Tools.Assert import *
from PyQuantum.Common.Matrix import *
# -------------------------------------------------------------------------------------------------
from scipy.sparse.linalg import norm

# -------------------------------------------------------------------------------------------------


class WaveFunction(Matrix):

    # ---------------------------------------------------------------------------------------------
    def __init__(self, states, init_state, amplitude=1):
        # Assert(isinstance(states, dict), "states is not dict")
        Assert(isinstance(init_state, list), "init_state is not list")

        Assert(len(states) > 1, "w_0 is not set")

        self.states = states
        self.init_state = init_state
        self.amplitude = amplitude

        k_found = None

        for k, v in enumerate(states):
            if init_state == v:
                k_found = k

                break

        Assert(k_found is not None, "w_0 is not set")

        super(WaveFunction, self).__init__(
            m=len(states), n=1, dtype=np.complex128)

        self.data[k_found, 0] = amplitude
    # ---------------------------------------------------------------------------------------------

    def set_ampl(self, state, amplitude=1):
        k_found = None

        for k, v in enumerate(self.states):
            if state == v:
                print("k_found =", k_found)
                break

        Assert(k_found is not None, "w_0 is not set")
        self.data[k_found, 0] = amplitude

    # ------------------------------------------------------------------------------------------
    def normalize(self):
        nnorm = norm(self.data)
        Assert(nnorm > 0, "norm <= 0")

        self.data /= nnorm
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    def print(self):
        for k, v in enumerate(self.states):
            amplitude = self.data[k, 0]

            if amplitude.imag == 0:
                if int(amplitude.real) == amplitude.real:
                    print(v, int(amplitude.real))
                else:
                    print(v, amplitude.real)
            else:
                print(v, amplitude)
    # ---------------------------------------------------------------------------------------------

    def __sub__(self, other):
        wf = copy.copy(self)

        wf.data -= other.data

        return wf

    def __add__(self, other):
        wf = copy.copy(self)

        wf.data += other.data

        return wf

    def __mul__(self, coeff):
        wf = copy.deepcopy(self)

        wf.data *= coeff

        return wf


# -------------------------------------------------------------------------------------------------
