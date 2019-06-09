# -------------------------------------------------------------------------------------------------
# scientific
import numpy as np
# -------------------------------------------------------------------------------------------------
# system
from math import sqrt
from PyQuantum.Common.html import *
import copy
# -------------------------------------------------------------------------------------------------
# Common
from PyQuantum.Common.Matrix import *
from PyQuantum.Common.Assert import *
from PyQuantum.Common.Print import *
from PyQuantum.Common.Tools import *
# -------------------------------------------------------------------------------------------------
from PyQuantum.TC.State import *
import html


def a_cross(ph):
    return sqrt(ph + 1)


def a(ph):
    return sqrt(ph)

# -------------------------------------------------------------------------------------------------


class Hamiltonian:

    def __init__(self, capacity, cavity):
        Assert(isinstance(capacity, int), "capacity is not integer", cf())
        Assert(capacity > 0, "capacity <= 0", cf())

        # Assert(isinstance(cavity, "BipartiteGeneral.Cavity.Cavity"), "capacity is not integer", cf())

        self.capacity = capacity
        self.cavity = cavity

        self.n_atoms = cavity.n_atoms

        self.wc = cavity.wc
        self.wa = cavity.wa
        self.g = cavity.g
        self.n_levels = cavity.n_levels
        self.states = self.get_states()
        self.get_states_bin()
        # self.print_states()

        self.size = len(self.states)

        self.matrix = Matrix(self.size, self.size, dtype=np.complex128)
        # self.matrix_html = np.empty([self.size, self.size], dtype=">U900")

        for i in range(self.size):
            i_state = self.states[i]

            i_ph = i_state[0]
            i_at = i_state[1]

            for j in range(self.size):
                j_state = self.states[j]

                j_ph = j_state[0]
                j_at = j_state[1]

                # self.matrix_html[i, j] = ""

                if i_state == j_state:
                    self.matrix.data[i, j] = self.wc * i_ph
                    # if(self.matrix_html[i][j] != ""):
                    # self.matrix_html[i][j] += "+"
                    # self.matrix_html[i][j] += "wc" + DOT() + str(i_ph) + " "

                    for n_ in range(len(i_at)):
                        if i_at[n_] != 0:
                            print(i, j, i_at[n_], self.wa * i_at[n_])
                            self.matrix.data[i, j] += self.wa * i_at[n_]
                            # self.matrix.data[i, j] += self.wa[n_] * i_at[n_]

                            # if(self.matrix_html[i][j] != ""):
                            # self.matrix_html[i][j] += "+"
                            # self.matrix_html[i][j] += "wa" + SUB(n_) + DOT() + str(i_at[n_]) + " "
                else:
                    d_ph = j_ph - i_ph

                    if abs(d_ph) == 1:
                        diff_at_cnt = 0

                        for n_ in range(len(i_at)):
                            d_at = j_at[n_] - i_at[n_]

                            if d_ph + d_at == 0:
                                diff_at_cnt += 1
                                diff_at_num = n_
                            elif d_at != 0:
                                diff_at_cnt = 0
                                break

                            if diff_at_cnt > 1:
                                break

                        if diff_at_cnt == 1:
                            if d_ph > 0:
                                k = a_cross(i_ph) * i_at[diff_at_num]

                                self.matrix.data[i,
                                                 j] = self.g * k
                                # j] = self.g[diff_at_num] * k
                                # self.matrix_html[i][j] = "g" + SUB(diff_at_num) + DOT() + A_CROSS(i_ph) + \
                                # """<math display="block"><mrow><msqrt><mn> &middot; """ + \
                                # A_CROSS(i_ph) + """</mn></msqrt><mo>=</mo></mrow></math>"""
                            else:
                                k = a_cross(j_ph) * j_at[diff_at_num]

                                # print(k)
                                # print(diff_at_num)
                                # print(self.g)
                                # print(self.g[diff_at_num])
                                self.matrix.data[i,
                                                 # j] = self.g[diff_at_num] * k
                                                 j] = self.g * k
                                # self.matrix_html[i][j] = "g" + SUB(diff_at_num) + DOT() + A_CROSS(j_ph)

        self.matrix.check_hermiticity()

        return
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    def print_html(self, filename):
        states = self.states
        return
    # -------------------------------------------------------------------------------------------------

    def to_html(self, filename):
        self.matrix.states = self.states
        print(self.matrix.data)
        print(self.matrix.m, self.matrix.n)
        self.matrix.to_html(filename)

    # -------------------------------------------------------------------------------------------------
    def to_csv(self, filename):
        self.matrix.to_csv(filename)

        return
    # -------------------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------------------
    def get_states(self):
        self.states = {}

        # state = [0, [0] * self.n_atoms]
        # state = [self.capacity, [0] * self.n_atoms]
        cnt = 0
        state = State(self.capacity, self.n_atoms, self.n_levels)

        # self.states[cnt] = copy.deepcopy(state)
        # cnt += 1

        # state[0] -= 1

        while(state.inc()):
            if state.state[0] + np.sum(state.state[1]) == self.capacity:
                # print("cnt:", cnt, state.state)
                self.states[cnt] = copy.deepcopy(state.state)
                cnt += 1

        # print(self.states)
        # exit(0)
        # while(1):
        #     inced = False

        #     for n_ in range(self.n_atoms - 1, -1, -1):
        #         if state[1][n_] == self.n_levels-1:
        #             state[1][n_] = 0

        #             continue

        #         if state[0] + np.sum(state[1]) > self.capacity:
        #             continue

        #         state[1][n_] += 1

        #         inced = True

        #         state[0] = self.capacity - np.sum(state[1])

        #         if state[0] >= 0:
        #             self.states[cnt] = copy.deepcopy(state)
        #             print("cnt=", cnt, self.states[cnt])
        #             cnt += 1

        #         break

        #     if not inced:
        #         break

        print(55)
        self.check_states()
        print(66)
        # self.states_rev = {}

        # for k, v in self.states.items():
        #     self.states_rev[len(self.states)-1-k] = v

        # print(self.states)
        # self.states = self.states_rev
        # print(self.states_rev)
        return self.states
    # -------------------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------------------
    def check_states(self):
        try:
            Assert(len(self.states) > 0, "len(states) <= 0", cf())

            for state in self.states.values():
                ph = state[0]
                at = state[1]

                Assert(0 <= ph <= self.capacity,
                       "incorrect state " + str(state), cf())
                Assert(ph + np.sum(at) == self.capacity,
                       "incorrect state " + str(state), cf())
                for n_ in range(len(at)):
                    Assert(0 <= at[n_] <= self.n_levels,
                           "incorrect state " + str(state), cf())
        except:
            print_error("incorrect states generation", cf())
            exit(1)

        return
    # -------------------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------------------
    def print_states(self):
        print("Hamiltonian states", color="green")

        try:
            for v in self.states.values():
                print("[%2d, " % (v[0]), v[1], "]", sep="")

            print()
        except:
            print_error("states not set", cf())
            exit(1)

        return
    # -------------------------------------------------------------------------------------------------

    def print_bin_states(self):
        for k, v in self.states_bin.items():
            print(k, v)

    def get_states_bin(self):
        states_bin = {}

        for k, v in self.states.items():
            at_state = v[1]

            en1 = at_state[: int(self.n_atoms / 2)]
            en2 = at_state[int(self.n_atoms / 2):]

            st = "[" + str(np.sum(en1)) + "," + str(np.sum(en2)) + "]"

            if not st in states_bin.keys():
                states_bin[st] = []

            states_bin[st].append(k)

        self.states_bin = {}
        self.states_bin_keys = []

        for k1 in range(int(self.n_atoms / 2) + 1):
            for k2 in range(int(self.n_atoms / 2) + 1):
                if k1 + k2 > self.capacity:
                    break

                k = "[" + str(k1) + "," + str(k2) + "]"

                self.states_bin_keys.append(k)

                if k in states_bin.keys():
                    self.states_bin[k] = states_bin[k]

        self.states_bin_keys = sorted(self.states_bin_keys)
        return self.states_bin
