from math import sqrt
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.TC3
from PyQuantum.TC3_sink.Cavity import Cavity
from PyQuantum.TC3_sink.Hamiltonian import Hamiltonian
from PyQuantum.TC3_sink.WaveFunction import WaveFunction
import PyQuantum.TC3_Lindblad.config as config
# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
def get_H_10_000():
    n_atoms = 3
    n_levels = 3

    H_10_000 = Hamiltonian(
        capacity={
            '0_1': 1,
            '1_2': 0,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
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
        init_state=[1, 0, [0, 0, 0], [0, 0]]
    )

def get_H_01_000():
    n_atoms = 3
    n_levels = 3

    H_01_000 = Hamiltonian(
        capacity={
            '0_1': 0,
            '1_2': 1,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
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

    return H_01_000


def get_w0_01_000(H_01_000):
    return WaveFunction(
        states=H_01_000.states,
        init_state=[0, 1, [0, 0, 0], [0, 0]]
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
                '1_2': config.wc,
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
        init_state=[1, 1, [0, 0, 0], [0, 0]]
    )
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
def get_H_10_0D():
    n_atoms = 3
    n_levels = 3

    H_10_0D = Hamiltonian(
        capacity={
            '0_1': 2,
            '1_2': 0,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        # iprint=False
    )

    return H_10_0D


def get_w0_10_0D(H_10_0D):
    return \
        WaveFunction(states=H_10_0D.states, init_state=[1, 0, [0, 0, 1], [0, 0]], amplitude=1./sqrt(2)) - \
        WaveFunction(states=H_10_0D.states, init_state=[
                     1, 0, [0, 1, 0], [0, 0]], amplitude=1./sqrt(2))

def get_H_01_0D():
    n_atoms = 3
    n_levels = 3

    H_01_0D = Hamiltonian(
        capacity={
            '0_1': 1,
            '1_2': 1,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        # iprint=False
    )

    return H_01_0D


def get_w0_01_0D(H_01_0D):
    return \
        WaveFunction(states=H_01_0D.states, init_state=[0, 1, [0, 0, 1], [0, 0]], amplitude=1./sqrt(2)) - \
        WaveFunction(states=H_01_0D.states, init_state=[
                     0, 1, [0, 1, 0], [0, 0]], amplitude=1./sqrt(2))

def get_H_11_0D():
    n_atoms = 3
    n_levels = 3

    H_11_0D = Hamiltonian(
        capacity={
            '0_1': 2,
            '1_2': 1,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        # iprint=False
    )

    return H_11_0D


def get_w0_11_0D(H_11_0D):
    return \
        WaveFunction(states=H_11_0D.states, init_state=[1, 1, [0, 0, 1], [0, 0]], amplitude=1./sqrt(2)) - \
        WaveFunction(states=H_11_0D.states, init_state=[
                     1, 1, [0, 1, 0], [0, 0]], amplitude=1./sqrt(2))
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
def get_H_10_1D():
    n_atoms = 3
    n_levels = 3

    H_10_0D = Hamiltonian(
        capacity={
            '0_1': 2,
            '1_2': 0,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        # iprint=False
    )

    return H_10_0D


def get_w0_10_1D(H_10_1D):
    return \
        WaveFunction(states=H_10_1D.states, init_state=[1, 0, [0, 0, 1], [0, 0]], amplitude=1./sqrt(2)) - \
        WaveFunction(states=H_10_1D.states, init_state=[
                     1, 0, [1, 0, 0], [0, 0]], amplitude=1./sqrt(2))

def get_H_01_1D():
    n_atoms = 3
    n_levels = 3

    H_01_0D = Hamiltonian(
        capacity={
            '0_1': 1,
            '1_2': 1,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        # iprint=False
    )

    return H_01_0D


def get_w0_01_1D(H_01_1D):
    return \
        WaveFunction(states=H_01_1D.states, init_state=[0, 1, [0, 0, 1], [0, 0]], amplitude=1./sqrt(2)) - \
        WaveFunction(states=H_01_1D.states, init_state=[
                     0, 1, [1, 0, 0], [0, 0]], amplitude=1./sqrt(2))

def get_H_11_1D():
    n_atoms = 3
    n_levels = 3

    H_11_0D = Hamiltonian(
        capacity={
            '0_1': 2,
            '1_2': 1,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        # iprint=False
    )

    return H_11_0D


def get_w0_11_1D(H_11_1D):
    return \
        WaveFunction(states=H_11_1D.states, init_state=[1, 1, [0, 0, 1], [0, 0]], amplitude=1./sqrt(2)) - \
        WaveFunction(states=H_11_1D.states, init_state=[
                     1, 1, [1, 0, 0], [0, 0]], amplitude=1./sqrt(2))
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
def get_H_10_2D():
    n_atoms = 3
    n_levels = 3

    H_10_2D = Hamiltonian(
        capacity={
            '0_1': 2,
            '1_2': 0,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        # iprint=False
    )

    return H_10_2D


def get_w0_10_2D(H_10_2D):
    return \
        WaveFunction(states=H_10_2D.states, init_state=[1, 0, [0, 1, 0], [0, 0]], amplitude=1./sqrt(2)) - \
        WaveFunction(states=H_10_2D.states, init_state=[
                     1, 0, [1, 0, 0], [0, 0]], amplitude=1./sqrt(2))

def get_H_01_2D():
    n_atoms = 3
    n_levels = 3

    H_01_2D = Hamiltonian(
        capacity={
            '0_1': 1,
            '1_2': 1,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        # iprint=False
    )

    return H_01_2D


def get_w0_01_2D(H_01_2D):
    return \
        WaveFunction(states=H_01_2D.states, init_state=[0, 1, [0, 1, 0], [0, 0]], amplitude=1./sqrt(2)) - \
        WaveFunction(states=H_01_2D.states, init_state=[
                     0, 1, [1, 0, 0], [0, 0]], amplitude=1./sqrt(2))

def get_H_11_2D():
    n_atoms = 3
    n_levels = 3

    H_11_2D = Hamiltonian(
        capacity={
            '0_1': 2,
            '1_2': 1,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        # iprint=False
    )

    return H_11_2D


def get_w0_11_2D(H_11_2D):
    return \
        WaveFunction(states=H_11_2D.states, init_state=[1, 1, [0, 1, 0], [0, 0]], amplitude=1./sqrt(2)) - \
        WaveFunction(states=H_11_2D.states, init_state=[
                     1, 1, [1, 0, 0], [0, 0]], amplitude=1./sqrt(2))
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
def get_H_11_D():
    n_atoms = 3
    n_levels = 3

    H_11_D = Hamiltonian(
        capacity={
            '0_1': 3,
            '1_2': 2,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        # iprint=False
    )

    return H_11_D


def get_w0_11_D(H_11_D):
    return \
        WaveFunction(states=H_11_D.states, init_state=[1, 1, [0, 1, 2], [0, 0]], amplitude=1./sqrt(6)) + \
        WaveFunction(states=H_11_D.states, init_state=[1, 1, [1, 2, 0], [0, 0]], amplitude=1./sqrt(6)) + \
        WaveFunction(states=H_11_D.states, init_state=[1, 1, [2, 0, 1], [0, 0]], amplitude=1./sqrt(6)) - \
        WaveFunction(states=H_11_D.states, init_state=[1, 1, [0, 2, 1], [0, 0]], amplitude=1./sqrt(6)) - \
        WaveFunction(states=H_11_D.states, init_state=[1, 1, [1, 0, 2], [0, 0]], amplitude=1./sqrt(6)) - \
        WaveFunction(states=H_11_D.states, init_state=[1, 1, [2, 1, 0], [0, 0]], amplitude=1./sqrt(6))


def get_H_10_D():
    n_atoms = 3
    n_levels = 3

    H_10_D = Hamiltonian(
        capacity={
            '0_1': 3,
            '1_2': 1,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        # iprint=False
    )

    return H_10_D


def get_w0_10_D(H_10_D):
    return \
        WaveFunction(states=H_10_D.states, init_state=[1, 0, [0, 1, 2], [0, 0]], amplitude=1./sqrt(6)) + \
        WaveFunction(states=H_10_D.states, init_state=[1, 0, [1, 2, 0], [0, 0]], amplitude=1./sqrt(6)) + \
        WaveFunction(states=H_10_D.states, init_state=[1, 0, [2, 0, 1], [0, 0]], amplitude=1./sqrt(6)) - \
        WaveFunction(states=H_10_D.states, init_state=[1, 0, [0, 2, 1], [0, 0]], amplitude=1./sqrt(6)) - \
        WaveFunction(states=H_10_D.states, init_state=[1, 0, [1, 0, 2], [0, 0]], amplitude=1./sqrt(6)) - \
        WaveFunction(states=H_10_D.states, init_state=[1, 0, [2, 1, 0], [0, 0]], amplitude=1./sqrt(6))

def get_H_01_D():
    n_atoms = 3
    n_levels = 3

    H_01_D = Hamiltonian(
        capacity={
            '0_1': 2,
            '1_2': 2,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        # iprint=False
    )

    return H_01_D


def get_w0_01_D(H_01_D):
    return \
        WaveFunction(states=H_01_D.states, init_state=[0, 1, [0, 1, 2], [0, 0]], amplitude=1./sqrt(6)) + \
        WaveFunction(states=H_01_D.states, init_state=[0, 1, [1, 2, 0], [0, 0]], amplitude=1./sqrt(6)) + \
        WaveFunction(states=H_01_D.states, init_state=[0, 1, [2, 0, 1], [0, 0]], amplitude=1./sqrt(6)) - \
        WaveFunction(states=H_01_D.states, init_state=[0, 1, [0, 2, 1], [0, 0]], amplitude=1./sqrt(6)) - \
        WaveFunction(states=H_01_D.states, init_state=[0, 1, [1, 0, 2], [0, 0]], amplitude=1./sqrt(6)) - \
        WaveFunction(states=H_01_D.states, init_state=[0, 1, [2, 1, 0], [0, 0]], amplitude=1./sqrt(6))
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def get_H_00_D():
    n_atoms = 3
    n_levels = 3

    H_00_D = Hamiltonian(
        capacity={
            '0_1': 2,
            '1_2': 1,
        },
        cavity=Cavity(
            wc={
                '0_1': config.wc,
                '1_2': config.wc,
            },
            wa=[config.wa]*n_atoms,
            g={
                '0_1': config.g,
                '1_2': config.g,
            },
            n_atoms=n_atoms,
            n_levels=n_levels
        ),
        # iprint=False
    )

    return H_00_D


def get_w0_00_D(H_00_D):
    return \
        WaveFunction(states=H_00_D.states, init_state=[0, 0, [0, 1, 2], [0, 0]], amplitude=1./sqrt(6)) + \
        WaveFunction(states=H_00_D.states, init_state=[0, 0, [1, 2, 0], [0, 0]], amplitude=1./sqrt(6)) + \
        WaveFunction(states=H_00_D.states, init_state=[0, 0, [2, 0, 1], [0, 0]], amplitude=1./sqrt(6)) - \
        WaveFunction(states=H_00_D.states, init_state=[0, 0, [0, 2, 1], [0, 0]], amplitude=1./sqrt(6)) - \
        WaveFunction(states=H_00_D.states, init_state=[0, 0, [1, 0, 2], [0, 0]], amplitude=1./sqrt(6)) - \
        WaveFunction(states=H_00_D.states, init_state=[0, 0, [2, 1, 0], [0, 0]], amplitude=1./sqrt(6))
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
