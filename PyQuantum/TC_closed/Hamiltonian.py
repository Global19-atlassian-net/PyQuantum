# ---------------------------------------------------------------------------------------------------------------------
# system
# ---------------------------------------------------------------------------------------------------------------------
# scientific
import numpy as np
import pandas as pd
from scipy.sparse import identity, kron, csc_matrix
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.TC
from PyQuantum.TC.AtomicBase import *
from PyQuantum.TC.FullBase import *
from PyQuantum.TC.Basis import *
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Tools
from PyQuantum.Tools.Hz import *
from PyQuantum.Tools.Print import *
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Common
from PyQuantum.Common.Matrix import *
# ---------------------------------------------------------------------------------------------------------------------



class Hamiltonian(Matrix):
    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- INIT -------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, capacity, cavity, RWA=True, iprint=False, iprint_symb=False):
        self.capacity = capacity
        self.cavity = cavity

        basis = Basis(capacity, cavity.n_atoms, cavity.n_levels)

        self.states = basis.basis

        # -------------------------------------------------------------------------------------------------------------
        self.H0 = self.H0(
            capacity, cavity.n_atoms, cavity.n_levels, cavity.wc, cavity.wa, cavity.g)

        self.H1 = self.H1(
            capacity, cavity.n_atoms, cavity.n_levels, cavity.wc, cavity.wa, cavity.g)

        if RWA:
            self.HI = self.HI_RWA(
                capacity, cavity.n_atoms, cavity.n_levels, cavity.wc, cavity.wa, cavity.g)
        else:
            self.HI = self.HI_EXACT(
                capacity, cavity.n_atoms, cavity.n_levels, cavity.wc, cavity.wa, cavity.g)

        Assert(np.shape(self.H0) == np.shape(self.H1), "size mismatch")
        Assert(np.shape(self.H1) == np.shape(self.HI), "size mismatch")

        self.data = self.H0 + self.H1 + self.HI
        self.cut_states(capacity)
        self.print_states()

        self.size = np.shape(self.data)[0]

        # super(Hamiltonian, self).__init__(
        #     self.size=np.shape(self.data)[0]
        #     m=self.size, n=self.size, dtype=np.longdouble)

        # self.data = self.H0
        # self.data = self.H1
        # self.data = self.HI

        self.get_states_bin()

        is_hermitian = np.all(self.data.todense().getH() ==
                              self.data.todense())
        Assert(is_hermitian, 'H is not hermitian')

        if iprint_symb:
            self.iprint_symb('H3_symb.html')

        if iprint:
            self.iprint('H3.html')
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------



    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- STATES -----------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def cut_states(self, capacity):
        to_rm = []

        for i in range(len(self.states)):
            if self.states[i][0] + np.sum(self.states[i][1]) > capacity:
                to_rm.append(i)

        self.data = self.data.toarray()

        for i in to_rm[::-1]:
            self.data = np.delete(self.data, i, axis=0)
            self.data = np.delete(self.data, i, axis=1)

            del self.states[i]

        self.data = csc_matrix(self.data)

    def get_states_bin(self):
        states_bin = {}

        for k, v in enumerate(self.states):
            en = v[0] + np.sum(v[1])

            if en not in states_bin:
                states_bin[en] = []

            states_bin[en].append(k)

        self.states_bin = states_bin
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------



    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- H0 ---------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def H0(self, capacity, at_count, n_levels, wc, wa, g):
        # -----------------------------------------
        adiag = np.sqrt(np.arange(1, capacity + 1))

        across = np.diagflat(adiag, -1)
        a = np.diagflat(adiag, 1)
        acrossa = np.dot(across, a)
        # -----------------------------------------

        # ----------------------------------------------
        H_dim = (capacity + 1) * pow(n_levels, at_count)

        at_dim = pow(n_levels, at_count)
        # ----------------------------------------------

        I_at = identity(at_dim)

        H0 = csc_matrix((H_dim, H_dim))
        H0 += wc * kron(acrossa, I_at)

        return H0
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------



    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- H1_RWA -----------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def H1(self, capacity, at_count, n_levels, wc, wa, g):
        # -----------------------------------------
        sigmadiag = range(1, n_levels)
        sigmacross = np.diagflat(sigmadiag, -1)
        sigma = np.diagflat(sigmadiag, 1)
        sigmacrosssigma = np.dot(sigmacross, sigma)
        # -----------------------------------------
        
        ph_dim = capacity + 1

        I_ph = identity(ph_dim)
        
        # ----------------------------------------------
        H_dim = (capacity + 1) * pow(n_levels, at_count)

        H1 = csc_matrix((H_dim, H_dim))
        # ----------------------------------------------

        for i in range(1, at_count + 1):
            elem = sigmacrosssigma

            at_prev = identity(pow(n_levels, i - 1))
            elem = kron(at_prev, elem)

            at_next = identity(pow(n_levels, at_count - i))
            elem = kron(elem, at_next)

            H1 += wa * kron(I_ph, elem)

        return H1
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    


    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- HI_RWA -----------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def HI_RWA(self, capacity, at_count, n_levels, wc, wa, g):
        # -----------------------------------------
        adiag = np.sqrt(np.arange(1, capacity + 1))

        across = np.diagflat(adiag, -1)
        a = np.diagflat(adiag, 1)
        acrossa = np.dot(across, a)
        # -----------------------------------------

        # -----------------------------------------
        sigmadiag = range(1, n_levels)

        sigmacross = np.diagflat(sigmadiag, -1)
        sigma = np.diagflat(sigmadiag, 1)
        sigmacrosssigma = np.dot(sigmacross, sigma)
        # -----------------------------------------
        
        # ----------------------------------------------
        H_dim = (capacity + 1) * pow(n_levels, at_count)

        HI = csc_matrix((H_dim, H_dim))
        # ----------------------------------------------
        
        for i in range(1, at_count + 1):
            # ------------------------------------------------
            elem = across

            before = identity(pow(n_levels, i - 1))
            elem = kron(elem, before)

            elem = kron(elem, sigma)

            after = identity(pow(n_levels, at_count - i))
            elem = kron(elem, after)

            HI += g * elem
            # ------------------------------------------------
            elem = a

            before = identity(pow(n_levels, i - 1))
            elem = kron(elem, before)

            elem = kron(elem, sigmacross)

            after = identity(pow(n_levels, at_count - i))
            elem = kron(elem, after)

            HI += g * elem

        return HI
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------



    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- PRINT STATES -----------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def print_states(self):
        cprint("Basis:\n", "green")

        for i in self.states:
            print(i)

        print()
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    


    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- PRINT ------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def print(self):
        for i in range(self.size):
            for j in range(self.size):
                print(round(self.data[i, j] / self.cavity.wc, 3), end='\t')
                # print(to_Hz(self.data[i, j]), end='\t')

            print()
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------



    # -----------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------- IPRINT -----------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    def iprint(self, filename='H3.html'):
        df = pd.DataFrame()

        data = self.data.toarray()

        for i in range(self.size):
            for j in range(self.size):
                if abs(data[i, j] != 0):
                    df.loc[i, j] = to_Hz(abs(data[i, j]))
                else:
                    df.loc[i, j] = ''

        df.index = df.columns = [str(v) for v in self.states]

        self.df = df
        self.df.to_html(filename)
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

# =====================================================================================================================
