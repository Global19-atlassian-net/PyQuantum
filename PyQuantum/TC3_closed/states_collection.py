# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.TC3
from PyQuantum.TC3.Cavity import Cavity
from PyQuantum.TC3.Hamiltonian import Hamiltonian
from PyQuantum.TC3_Lindblad.WaveFunction import WaveFunction
import PyQuantum.TC3_Lindblad.config as config
# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
def get_H_10_000():
    n_atoms = 3
    n_levels = 3

    H_10_000 = Hamiltonian(
        capacity={
            '0_1': 1,
            '1_2': 1,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc * 2,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        iprint=False
    )

    return H_10_000


def get_w0_10_000(H_10_000):
    return WaveFunction(
        states=H_10_000.states,
        init_state=[1, 0, [0, 0, 0]]
    )
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------


def get_H_11_000():
    n_atoms = 3
    n_levels = 3

    H_11_000 = Hamiltonian(
        capacity={
            '0_1': 1,
            '1_2': 1,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc * 2,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        iprint=False
    )

    return H_11_000


def get_w0_11_000(H_11_000):
    return WaveFunction(
        states=H_11_000.states,
        init_state=[1, 1, [0, 0, 0]]
    )
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
