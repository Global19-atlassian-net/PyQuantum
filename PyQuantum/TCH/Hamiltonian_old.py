import numpy as np
from PyQuantum.Common.Print import *
from PyQuantum.TCH.State import *
from PyQuantum.TCH.CavityChain import *
import copy
from PyQuantum.Common.Matrix import *
import PyQuantum.TC.Hamiltonian as H1


def cartesian_product(*arrays):
    la = len(arrays)
    dtype = np.result_type(*arrays)
    arr = np.empty([len(a) for a in arrays] + [la], dtype=dtype)
    for i, a in enumerate(np.ix_(*arrays)):
        arr[..., i] = a
    return arr.reshape(-1, la)


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
    def __init__(self, capacity, cv_chain, RWA=True):
        Assert(isinstance(capacity, int), "capacity is not integer", cf())
        Assert(capacity > 0, "capacity <= 0", cf())

        Assert(isinstance(cv_chain, CavityChain),
               "cv_chain is not CavityChain", cf())
        # for cv in cavities:
        #     Assert(isinstance(cv_chain, CavityChain),
        #            "cavity is not Cavity", cf())

        self.capacity = capacity
        self.cavity = cavity
        self.n = cavity.n

        self.get_states()

        # self.size = len(self.states)
        # self.matrix = Matrix(self.size, self.size, dtype=np.complex128)

        # # ------------------------------------------------------------------------------------------------------------------
        # H_field = self.get_H_field()
        # H_atoms = self.get_H_atoms()

        # H = H_field + H_atoms

        # if RWA:
        #     h1 = H1(cv_chain.cavity(0).capacity, cv_chain.cavity(0).n,
        #             cv_chain.cavity(0).wc, cv_chain.cavity(0).wa, cv_chain.cavity(0).g, RWA)
        #     # h2 = H1.get_H_RWA(ph_count2, at_count2, wc2, wa2, g2, RWA)
        #     H += self.get_H_int_RWA()
        # else:
        #     H += self.get_H_int_EXACT()

        # self.matrix.data = np.matrix(H)
        # ------------------------------------------------------------------------------------------------------------------

    def get_H_field(self):
        # ------------------------------------------------------------------------------------------------------------------
        acrossa = AcrossA(self.capacity)
        # ------------------------------------------------------------------------------------------------------------------
        H_dim = (self.capacity+1) * pow(2, self.cavity.n)
        # ------------------------------------------------------------------------------------------------------------------
        at_dim = pow(2, self.cavity.n)

        I_at = np.identity(at_dim)
        # ------------------------------------------------------------------------------------------------------------------
        H_field = self.cavity.wc * np.kron(acrossa, I_at)

        # ------------------------------------------------------------------------------------------------------------------
        return H_field

    def get_H_atoms(self):
        # ------------------------------------------------------------------------------------------------------------------
        sigmadiag = [1]

        sigmacross = np.diagflat(sigmadiag, -1)
        sigma = np.diagflat(sigmadiag, 1)
        sigmacrosssigma = np.dot(sigmacross, sigma)
        # ------------------------------------------------------------------------------------------------------------------
        ph_dim = self.capacity+1

        I_ph = np.identity(ph_dim)
        # ------------------------------------------------------------------------------------------------------------------
        H_dim = (self.capacity+1) * pow(2, self.cavity.n)

        H_atoms = np.zeros([H_dim, H_dim])
        # ------------------------------------------------------------------------------------------------------------------
        for i in range(1, self.cavity.n+1):
            elem = sigmacrosssigma

            at_prev = np.identity(pow(2, i-1))
            elem = np.kron(at_prev, elem)

            at_next = np.identity(pow(2, self.cavity.n-i))
            elem = np.kron(elem, at_next)

            H_atoms += self.cavity.wa * np.kron(I_ph, elem)
        # ------------------------------------------------------------------------------------------------------------------
        return H_atoms

    def get_H_int_RWA(self):
        # ------------------------------------------------------------------------------------------------------------------
        across = Across(self.capacity)
        a = A(self.capacity)
        acrossa = AcrossA(self.capacity)
        # ------------------------------------------------------------------------------------------------------------------
        sigmadiag = [1]

        sigmacross = np.diagflat(sigmadiag, -1)
        sigma = np.diagflat(sigmadiag, 1)
        sigmacrosssigma = np.dot(sigmacross, sigma)
        # ------------------------------------------------------------------------------------------------------------------
        H_dim = (self.capacity+1) * pow(2, self.cavity.n)

        H_int = np.zeros([H_dim, H_dim])
        # ------------------------------------------------------------------------------------------------------------------
        for i in range(1, self.cavity.n+1):
            # ------------------------------------------------
            elem = across

            before = np.identity(pow(2, i-1))
            elem = np.kron(elem, before)

            elem = np.kron(elem, sigma)

            after = np.identity(pow(2, self.cavity.n-i))
            elem = np.kron(elem, after)

            H_int += self.cavity.g * elem
            # ------------------------------------------------
            elem = a

            before = np.identity(pow(2, i-1))
            elem = np.kron(elem, before)

            elem = np.kron(elem, sigmacross)

            after = np.identity(pow(2, self.cavity.n-i))
            elem = np.kron(elem, after)

            H_int += self.cavity.g * elem
            # ------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------------
        return H_int

    def get_H_int_EXACT(self):
        # ------------------------------------------------------------------------------------------------------------------
        across = Across(self.capacity)
        a = A(self.capacity)
        acrossa = np.dot(across, a)
        # ------------------------------------------------------------------------------------------------------------------
        sigmadiag = [1]

        sigmacross = np.diagflat(sigmadiag, -1)
        sigma = np.diagflat(sigmadiag, 1)
        sigmacrosssigma = np.dot(sigmacross, sigma)
        # ------------------------------------------------------------------------------------------------------------------
        H_dim = (self.capacity+1) * pow(2, self.cavity.n)

        H_int = np.zeros([H_dim, H_dim], dtype=complex)
        # ------------------------------------------------------------------------------------------------------------------
        for i in range(1, self.cavity.n+1):
            # ------------------------------------------------
            elem = (across + a)

            before = np.identity(pow(2, i-1))
            elem = np.kron(elem, before)

            elem = np.kron(elem, sigmacross + sigma)

            after = np.identity(pow(2, self.cavity.n-i))
            elem = np.kron(elem, after)

            H_int += self.cavity.g * elem
            # ------------------------------------------------
        # ------------------------------------------------------------------------------------------------------------------
        return H_int

    # ---------------------------------------------------------------------------------------------
    def get_states(self):
        a = [0]
        # a = np.matrix([0])
        # a = np.matrix([[1, 0], [0, 1]])
        print(a)

        # b = np.matrix([[1, 0], [0, 1]])
        b = [1]
        # b = np.matrix([1])
        print(b)

        c = np.meshgrid(a, b)
        print(c)

        print(cartesian_product([0, 1], [0, 1]))
        exit(0)
        self.states = {}
        pass
        # state = State(self.capacity, self.cavity.n)

        # cnt = 0
        # self.states[cnt] = copy.copy(state.state())

        # while state.inc():
        #     cnt += 1
        #     self.states[cnt] = copy.copy(state.state())
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
    def write_to_file(self, filename):
        self.matrix.write_to_file(filename)
    # ---------------------------------------------------------------------------------------------


# import sys
# import numpy as np

# # from src.TCM.hamiltonian_err import *   # !DONE except err_msg
# import src.TCM.hamiltotian as H1


# def get_H(ph_count1, at_count1, wc1, wa1, g1, ph_count2, at_count2, wc2, wa2, g2, m=0.4, RWA=True):
#     #------------------------------------------------------------------------------------------------------------------
#     # get_H_err(ph_count, at_count, wc, wa, g, RWA)
#     #------------------------------------------------------------------------------------------------------------------
#     adiag1 = np.sqrt(np.arange(1, ph_count1+1))

#     across1 = np.diagflat(adiag1, -1)
#     a1 = np.diagflat(adiag1, 1)
#     acrossa1 = np.dot(across1, a1)

#     adiag2 = np.sqrt(np.arange(1, ph_count2+1))

#     across2 = np.diagflat(adiag2, -1)
#     a2 = np.diagflat(adiag2, 1)
#     acrossa2 = np.dot(across2, a2)
#     #------------------------------------------------------------------------------------------------------------------
#     sigmadiag = [1]

#     sigmacross = np.diagflat(sigmadiag, -1)
#     sigma = np.diagflat(sigmadiag, 1)
#     sigmacrosssigma = np.dot(sigmacross, sigma)
#     #------------------------------------------------------------------------------------------------------------------
#     ph1_dim = ph_count1+1
#     I_ph1 = np.identity(ph1_dim)

#     at1_dim = pow(2, at_count1)
#     I_at1 = np.identity(at1_dim)

#     ph2_dim = ph_count2+1
#     I_ph2 = np.identity(ph2_dim)

#     at2_dim = pow(2, at_count2)
#     I_at2 = np.identity(at2_dim)
#     #------------------------------------------------------------------------------------------------------------------
#     if RWA:
#         h1 = H1.get_H_RWA(ph_count1, at_count1, wc1, wa1, g1, RWA)
#         h2 = H1.get_H_RWA(ph_count2, at_count2, wc2, wa2, g2, RWA)
#     else:
#         h1 = H1.get_H_EXACT(ph_count1, at_count1, wc1, wa1, g1)
#         h2 = H1.get_H_EXACT(ph_count2, at_count2, wc2, wa2, g2)

#     H = np.kron(h1, np.identity(h2.shape[0])) + np.kron(np.identity(h1.shape[0]), h2)

#     H1_m = np.kron(across1, np.identity(at1_dim))
#     H1_m = np.kron(H1_m, a2)
#     H1_m = np.kron(H1_m, np.identity(at2_dim))

#     H2_m = np.kron(a1, np.identity(at1_dim))
#     H2_m = np.kron(H2_m, across2)
#     H2_m = np.kron(H2_m, np.identity(at2_dim))

#     H_m = m * (H1_m + H2_m)
#     #------------------------------------------------------------------------------------------------------------------
#     H = np.matrix(H + H_m)
#     H_size = np.shape(H)

#     # print('H:\n', H, '\n')
#     # # # print('H_size:', H_size, '\n')
#     #------------------------------------------------------------------------------------------------------------------
#     return H


# def write_to_file(H, filename):
#     #------------------------------------------------------------------------------------------------------------------
#     # write_to_file_err(H, filename)
#     #------------------------------------------------------------------------------------------------------------------
#     # fh = open(filename, 'w')
#     # #------------------------------------------------------------------------------------------------------------------
#     # fh.write(str(np.shape(H)[0]) + ' ')
#     # fh.write(str(np.shape(H)[1]) + ' ')
#     # fh.write('\n')

#     # for i in range(0, H.shape[0]):
#     #     for j in range(0, H.shape[0]):
#     #         elem = H.item(i, j)

#     #         fh.write(str(elem) + ' ')

#     #     fh.write('\n')
#     #------------------------------------------------------------------------------------------------------------------
#     precision = 5
#     eps = 1.0 / (10 ** precision)

#     print(H.shape)
#     for i in range(H.shape[0]-1, -1, -1):
#         is_null = True

#         for j in range(H.shape[1]-1, -1, -1):
#             if H.item(i, j) != 0:
#                 is_null = False
#                 break

#         if is_null:
#             print(i)
#             H = np.delete(H, i, axis=0)

#     for j in range(H.shape[1]-1, -1, -1):
#         is_null = True

#         for i in range(H.shape[0]-1, -1, -1):
#             if H.item(i, j) != 0:
#                 is_null = False
#                 break

#         if is_null:
#             H = np.delete(H, j, axis=1)

#     print(H.shape)
#     with open(filename, "w") as f:
#         for i in range(0, H.shape[0]):
#             for j in range(0, H.shape[1]):
#                 value = H.item(i, j)

#                 if abs(value.real) < eps:
#                     re = format(+0, "." + str(precision) + "f")
#                 else:
#                     re = format(value.real, "." + str(precision) + "f")

#                 if abs(value.imag) < eps:
#                     im = format(+0, "." + str(precision) + "f")
#                 else:
#                     im = format(value.imag, "." + str(precision) + "f")

#                 f.write("(" + re + "," + im + ")")

#                 if j != H.shape[1] - 1:
#                     f.write(",")

#             f.write("\n")
#     #------------------------------------------------------------------------------------------------------------------
#     return
