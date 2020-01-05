# ---------------------------------------------------------------------------------------------------------------------
# system
from math import sqrt
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.TC
from PyQuantum.TC.Cavity import Cavity
from PyQuantum.TC.Hamiltonian import Hamiltonian
from PyQuantum.TC_Lindblad.WaveFunction import WaveFunction
import PyQuantum.TC_Lindblad.config as config
# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
def get_H_1_00():
    n_atoms = 2
    n_levels = 2

    H_1_00 = Hamiltonian(
        capacity=1,
        cavity=Cavity(
            wc=config.wc,
            wa=config.wa,
            g=config.g,
            n_atoms=n_atoms,
        ),
        # iprint=False
    )

    return H_1_00


def get_w0_1_00(H_1_00):
    return WaveFunction(
        states=H_1_00.states,
        init_state=[1, [0, 0]]
    )
# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
def get_H_1_D():
    n_atoms = 2
    n_levels = 2

    H_1_D = Hamiltonian(
        capacity=2,
        cavity=Cavity(
            wc=config.wc,
            wa=config.wa,
            g=config.g,
            n_atoms=n_atoms,
        ),
        # iprint=False
    )

    return H_1_D


def get_w0_1_D(H_1_D):
    return \
        WaveFunction(states=H_1_D.states, init_state=[1, [0, 1]], amplitude=1./sqrt(2)) - \
        WaveFunction(states=H_1_D.states, init_state=[
                     1, [1, 0]], amplitude=1./sqrt(2))
# ---------------------------------------------------------------------------------------------------------------------

# n_levels = 3

# # |0⟩|0⟩|000⟩
# t_10_000 = WaveFunction(
#     states=Hamiltonian3(
#         capacity={
#             '0_1': 1,
#             '1_2': 0,
#         },
#         cavity=CavityN(
#             wc={
#                 '0_1': config.wc,
#                 '1_2': config.wc * 2,
#             },
#             wa=config.wa,
#             g={
#                 '0_1': config.g,
#                 '1_2': config.g,
#             },
#             n_atoms=3,
#             n_levels=n_levels
#         ),
#         iprint=False).states,
#     init_state=[1, 0, [0, 0, 0]]
# )

# t_01_000 = WaveFunction(
#     states=Hamiltonian3(
#         capacity={
#             '0_1': 0,
#             '1_2': 1,
#         },
#         cavity=CavityN(
#             wc={
#                 '0_1': config.wc,
#                 '1_2': config.wc * 2,
#             },
#             wa=config.wa,
#             g={
#                 '0_1': config.g,
#                 '1_2': config.g,
#             },
#             n_atoms=3,
#             n_levels=n_levels
#         ),
#         iprint=False).states,
#     init_state=[0, 1, [0, 0, 0]]
# )
