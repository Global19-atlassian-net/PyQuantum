import numpy as np
from PyQuantum.Common.Print import *
from PyQuantum.TCH.State import *
from PyQuantum.TCH.CavityChain import *
import copy
from PyQuantum.Common.Matrix import *
import PyQuantum.TC.Hamiltonian as H1
from PyQuantum.TCH.FullBase import *


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
    def diag(self, i, j):
        self.matrix.data[i, j] = 0

        value = []

        for cv in range(0, len(self.cv_chain.cavities)):
            self.matrix.data[i, j] += self.cv_chain.cavity(cv).wc * \
                self.states[i][cv][0]

            if self.states[i][cv][0] > 0:
                if self.states[i][cv][0] == 1:
                    value.append('wc'+str(cv+1))
                else:
                    value.append('wc'+str(cv+1) + '*' +
                                 str(self.states[i][cv][0]))

            at_sum = np.sum(self.states[i][cv][1])

            self.matrix.data[i, j] += self.cv_chain.cavity(cv).wa * \
                at_sum

            if at_sum > 0:
                if at_sum == 1:
                    value.append('wa'+str(cv+1))
                else:
                    value.append('wa'+str(cv+1) + '*' +
                                 str(at_sum))

        self.matrix_symb.data[i, j] = ' + '.join(value)
    # ---------------------------------------------------------------------------------------------

    def __init__(self, capacity, cv_chain, RWA, mu):
        Assert(isinstance(capacity, int), "capacity is not integer", cf())
        Assert(capacity > 0, "capacity <= 0", cf())

        Assert(isinstance(cv_chain, CavityChain),
               "cv_chain is not CavityChain", cf())
        # for cv in cavities:
        #     Assert(isinstance(cv_chain, CavityChain),
        #            "cavity is not Cavity", cf())

        self.capacity = capacity
        self.cv_chain = cv_chain
        # self.n = cavity.n

        self.get_states()

        self.size = len(self.states)
        # print("size =", self.size)
        # exit(0)
        self.matrix = Matrix(self.size, self.size, dtype=np.complex128)
        self.matrix_symb = Matrix(self.size, self.size, dtype=str)

        for i in range(self.size):
            i_state = self.states[i]

            for j in range(self.size):
                j_state = self.states[j]

                if i == j:
                    self.diag(i, j)
                else:
                    # # jump
                    ne_cv = []

                    ne_cnt = 0

                    for cv in range(0, len(self.cv_chain.cavities)):
                        if i_state[cv] != j_state[cv]:
                            ne_cnt += 1

                            if ne_cnt > 2:
                                break

                            ne_cv.append(cv)

                    if ne_cnt == 2:
                        d_ph_i = i_state[ne_cv[0]][0] - \
                            i_state[ne_cv[1]][0]
                        d_ph_j = j_state[ne_cv[0]][0] - \
                            j_state[ne_cv[1]][0]

                        if abs(d_ph_i) == 1 and d_ph_i == - d_ph_j \
                                and np.all(i_state[ne_cv[0]][1] == j_state[ne_cv[1]][1]):
                            # print(self.states[i], self.states[j])
                            # exit(0)
                            self.matrix.data[i, j] = mu
                            self.matrix_symb.data[i, j] = 'mu'
                            continue
                    elif ne_cnt == 1:
                        # g
                        at_i = i_state[ne_cv[0]][1]
                        at_j = j_state[ne_cv[0]][1]

                        ne_at_cnt = 0
                        ne_at_ind = []

                        for at_ind in range(0, len(at_i)):
                            if at_i[at_ind] != at_j[at_ind]:
                                ne_at_ind.append(at_ind)
                                ne_at_cnt += 1
                                ne_at = at_ind

                                if ne_at_cnt > 2:
                                    break

                        if ne_at_cnt == 2:
                            if at_i[ne_at_ind[0]] ^ at_i[ne_at_ind[1]]:
                                # print(at_i, at_j)
                                self.matrix.data[i, j] = self.cv_chain.cavity(
                                    ne_cv[0]).g
                                self.matrix_symb.data[i,
                                                      j] = 'g' + str(ne_cv[0]+1)
                                continue

                    self.matrix_symb.data[i, j] = '0'

        # self.matrix.data = np.matrix(H)
        # ------------------------------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------

    def get_states(self):
        states = get_full_base(
            capacity=self.capacity, cv_chain=self.cv_chain, limit=False)

        cnt = 0

        self.states = {}

        for i in states:
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

        df.to_html("H.html")
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    def write_to_file(self, filename):
        self.matrix.write_to_file(filename)
    # ---------------------------------------------------------------------------------------------
