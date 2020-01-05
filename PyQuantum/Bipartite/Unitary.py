# -------------------------------------------------------------------------------------------------
from PyQuantum.Bipartite.Hamiltonian import Hamiltonian
# -------------------------------------------------------------------------------------------------
# Common
from PyQuantum.Common.Matrix import *
# -------------------------------------------------------------------------------------------------
# scientific
import numpy as np
import scipy.linalg as lg
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
class Unitary(Matrix):

    # ---------------------------------------------------------------------------------------------
    def __init__(self, H, dt):
        Assert(isinstance(H, Hamiltonian),
               "H is not Hamiltonian", FILE(), LINE())
        Assert(isinstance(dt, (int, float)),
               "dt is not numeric", FILE(), LINE())

        Assert(dt > 0, "dt <= 0", FILE(), LINE())

        super(Unitary, self).__init__(m=H.size, n=H.size, dtype=np.complex128)

        # H_data = np.array(H.matrix.data, dtype=np.complex128)
        H.data = H.matrix.data
        self.data = lg.expm(-1j * H.data * dt)
        self.data = csc_matrix(self.data, dtype=np.complex128)

        # self.data = np.matrix(lg.expm(-1j * H_data * dt), dtype=np.complex128)
    # ---------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
