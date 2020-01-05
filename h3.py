from PyQuantum.TC3.Cavity import Cavity
from PyQuantum.TC3.Hamiltonian3 import Hamiltonian3

capacity = {
    '0_1': 2,
    '1_2': 2,
}

wc = {
    '0_1': 0.2,
    '1_2': 0.3,
}

wa = [0.2] * 3

g = {
    '0_1': 1,
    '1_2': 200,
}

cv = Cavity(wc=wc, wa=wa, g=g, n_atoms=3, n_levels=3)

# cv.wc_info()
# cv.wa_info()
# cv.g_info()

cv.info()
H = Hamiltonian3(capacity=capacity, cavity=cv, iprint=False)

H.print_states()
H.print_bin_states()
# H.iprint()
