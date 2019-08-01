import numpy as np
from PyQuantum.Common.Print import *
from PyQuantum.TC.State import *
from PyQuantum.TC.Cavity import *
import copy
from PyQuantum.Common.Matrix import *
from PyQuantum.TC.FullBase import *


def Across(capacity):
    Assert(capacity > 0, "capacity <= 0", cf())

    adiag = np.sqrt(np.arange(1, capacity+1))

    across = np.diagflat(adiag, -1)

    return across


def A(capacity):
    Assert(capacity > 0, "capacity <= 0", cf())

    adiag = np.sqrt(np.arange(1, capacity+1))

    a = np.diagflat(adiag, 1)

    return a


def AcrossA(capacity):
    Assert(capacity > 0, "capacity <= 0", cf())

    across = Across(capacity)
    a = A(capacity)

    acrossa = np.dot(across, a)

    return acrossa


class Hamiltonian:
    # ---------------------------------------------------------------------------------------------
    def __init__(self, capacity, cavity, RWA=True):
        Assert(isinstance(capacity, int), "capacity is not integer", cf())
        Assert(capacity > 0, "capacity <= 0", cf())

        Assert(isinstance(cavity, Cavity), "cavity is not Cavity", cf())

        self.capacity = capacity
        self.cavity = cavity
        self.n = cavity.n

        self.get_states()

        self.size = len(self.states)
        self.matrix = Matrix(self.size, self.size, dtype=np.complex128)

        self.matrix_symb = Matrix(self.size, self.size, dtype=str)

        for i, st1 in self.states.items():
            for j, st2 in self.states.items():
                if i == j:
                    self.matrix.data[i, j] = st1[0] * \
                        self.cavity.wc + np.sum(st1[1]) * self.cavity.wa

                    value = []

                    if st1[0] > 0:
                        if st1[0] == 1:
                            value.append('wc')
                        else:
                            value.append(str(st1[0]) + '*wc')

                    if np.sum(st1[1]) > 0:
                        if np.sum(st1[1]) == 1:
                            value.append('wa')
                        else:
                            value.append(str(np.sum(st1[1])) + '*wa')

                    self.matrix_symb.data[i, j] = ' + '.join(value)
                else:
                    if abs(st1[0]-st2[0]) == 1 and (st1[0]-st2[0]) + (np.sum(st1[1])-np.sum(st2[1])) == 0:
                        self.matrix.data[i, j] = self.cavity.g
                        self.matrix_symb.data[i, j] = 'g'
                    else:
                        self.matrix_symb.data[i, j] = '0'

    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    def get_states(self):
        atomic_base = AtomicBasis(count=self.capacity)

        full_base = Base(capacity=self.capacity, atomic_base=atomic_base)

        cnt = 0

        self.states = {}

        for i in full_base.base:
            self.states[cnt] = i
            cnt += 1

        self.states_str = list(self.states.values())
        self.states_str = [str(i) for i in self.states_str]
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    def print_states(self):
        print("States:", color="green")

        print()

        for k, v in self.states.items():
            print(v)

        print()
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    def print(self):
        print(self.matrix.data)
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    def iprint(self):
        import pandas as pd

        df = pd.DataFrame()

        for i in range(self.size):
            for j in range(self.size):
                df.loc[i, j] = wc_str(abs(self.matrix.data[i, j]))

        df.index = df.columns = self.states_str

        self.df = df
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    def iprint_symb(self):
        import pandas as pd

        df = pd.DataFrame()

        for i in range(self.size):
            for j in range(self.size):
                df.loc[i, j] = self.matrix_symb.data[i, j]

        df.index = df.columns = self.states_str

        self.df = df
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    def write_to_file(self, filename):
        self.matrix.write_to_file(filename)
    # ---------------------------------------------------------------------------------------------
