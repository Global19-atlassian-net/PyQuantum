# ---------------------------------------------------------------------------------------------------------------------
# system
import sys
from math import sqrt
# ---------------------------------------------------------------------------------------------------------------------
# scientific
import numpy as np
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.TC_Lindblad
from PyQuantum.TC_Lindblad.Cavity import Cavity
from PyQuantum.TC_Lindblad.Hamiltonian import Hamiltonian

from PyQuantum.TC_Lindblad.WaveFunction import WaveFunction
from PyQuantum.TC_Lindblad.DensityMatrix import DensityMatrix

from PyQuantum.TC_Lindblad.Evolution import run

import PyQuantum.TC_Lindblad.config as config
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.TC3
from PyQuantum.TC.states_collection import *
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
from PyQuantum.Common.Quantum.Operators import operator_a
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

H_1_00 = get_H_1_00()
w0_1_00 = get_w0_1_00(H_1_00)

H_1_D = get_H_1_D()
w0_1_D = get_w0_1_D(H_1_D)

# ---------------------------------------------------------------------------------------------------------------------
mkdir('sink')
mkdir('sink/1ms_l001g')
# ---------------------------------------------------------------------------------------------------------------------

for state in [
    {
        'name': '1_00',
        'w0': w0_1_00,
        'H': H_1_00,
    },
    {
        'name': '1_D',
        'w0': w0_1_D,
        'H': H_1_D,
    },
]:
    # -----------------------------------------------------------------------------------------------------------------
    state['w0'].normalize()

    ro_0 = DensityMatrix(state['w0'])

    T_list = []
    sink_list = []

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
            'out': {
                'L': operator_a(state['H']),
                'l': l
            },
        },
    })

    # MkDir('sink')
    pickle_dump(T_list, 'sink/1ms_l001g/T_list_' + state['name'] + '.pkl')
    pickle_dump(sink_list, 'sink/1ms_l001g/sink_list_' +
                state['name'] + '.pkl')
    # -----------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------

# =====================================================================================================================
