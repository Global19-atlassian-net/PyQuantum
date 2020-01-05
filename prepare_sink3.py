# ---------------------------------------------------------------------------------------------------------------------
# system
import sys
from math import sqrt
# ---------------------------------------------------------------------------------------------------------------------
# scientific
import numpy as np
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.TC_Lindblad
from PyQuantum.TC3_Lindblad.Cavity import Cavity
from PyQuantum.TC3_Lindblad.Hamiltonian import Hamiltonian

from PyQuantum.TC3_Lindblad.WaveFunction import WaveFunction
from PyQuantum.TC3_Lindblad.DensityMatrix import DensityMatrix

from PyQuantum.TC3_Lindblad.Evolution import run

import PyQuantum.TC3_Lindblad.config as config
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.TC3
from PyQuantum.TC3.states_collection import *
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Tools
from PyQuantum.Tools.LoadPackage import load_pkg
from PyQuantum.Tools.Assert import *
from PyQuantum.Tools.Print import hr
from PyQuantum.Tools.MkDir import *
from PyQuantum.Tools.CSV import *
from PyQuantum.Tools.Units import *
from PyQuantum.Tools.Pickle import *
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Common
from PyQuantum.Common.Quantum.Operators import operator_a3
# ---------------------------------------------------------------------------------------------------------------------

# -----------------------------------------------
l = config.g * 0.01

T = 1 * config.ms

# dt = 0.01 / l
# dt = 1 * config.ns
dt = 10 * config.ns
# dt = 1 * config.ns / 10
nt = int(T/dt)
# dt = (0.001/l)

# Assert(dt <= 0.01/l, 'dt > 0.01/l')

nt = int(T/dt)

cprint('T:', 'green', end='')
print(time_unit_full(T))

cprint('dt:', 'green', end='')
# print(time_unit_full(dt))

cprint('nt:', 'green', end='')
print(nt)
# -----------------------------------------------

H_10_000 = get_H_10_000()
w0_10_000 = get_w0_10_000(H_10_000)
# w0_10_000.print()

H_11_000 = get_H_11_000()
w0_11_000 = get_w0_11_000(H_11_000)


# ---------------------------------------------------------------------------------------------------------------------
mkdir('sink3')
mkdir('sink3/1ms_l001g')
# ---------------------------------------------------------------------------------------------------------------------

for state in [
    # {
    #     'name': '10_000',
    #     'w0': w0_10_000,
    #     'H': H_10_000,
    # },
    {
        'name': '11_000',
        'w0': w0_11_000,
        'H': H_11_000,
    },
]:
    # -----------------------------------------------------------------------------------------------------------------
    state['w0'].normalize()

    ro_0 = DensityMatrix(state['w0'])

    T_list = []
    sink_list = {'0_1': [], '1_2': []}

    run({
        "ro_0": ro_0,
        "H": state['H'],
        "dt": dt,
        "sink_list": sink_list,
        "T_list": T_list,
        "precision": 1e-3,
        'sink_limit': 1,
        "thres": 0.001,
        'lindblad': {
            'out': [
                {
                    'L': operator_a3(state['H'], ph_type=1),
                    'l': l
                },
                {
                    'L': operator_a3(state['H'], ph_type=2),
                    'l': l
                },
            ],
        },
    })

    # MkDir('sink')
    pickle_dump(T_list, 'sink3/1ms_l001g/T_list_' + state['name'] + '.pkl')
    # pickle_dump(sink_list, 'sink3/1ms_l001g/sink_list_' + w_0['name'] + '.pkl')
    pickle_dump(
        sink_list['0_1'], 'sink3/1ms_l001g/sink_list_' + state['name'] + '_01.pkl')
    pickle_dump(
        sink_list['1_2'], 'sink3/1ms_l001g/sink_list_' + state['name'] + '_12.pkl')
    # -----------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------

# =====================================================================================================================
