# ---------------------------------------------------------------------------------------------------------------------
# system
import sys
from math import sqrt
# ---------------------------------------------------------------------------------------------------------------------
# scientific
import numpy as np
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.TC_Lindblad_sink
from PyQuantum.TCL_sink.Cavity import Cavity
from PyQuantum.TCL_sink.Hamiltonian3 import Hamiltonian

from PyQuantum.TCL_sink.WaveFunction import WaveFunction
from PyQuantum.TCL_sink.DensityMatrix import DensityMatrix

from PyQuantum.TCL3_sink.Evolution import run

import PyQuantum.TCL_sink.config as config
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.TC3
from PyQuantum.TC3_sink.states_collection import *
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
from PyQuantum.Common.Quantum.Operators import operator_a3all, operator_a3all_new
# ---------------------------------------------------------------------------------------------------------------------
# exit(0)
# -----------------------------------------------
l = config.g * 0.5

T = 1 * config.ms

# dt = 0.01 / l
dt = 0.1 * config.ns
# dt = 10 * config.ns
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
# H_11_000 = get_H_11_000()
# w0_11_000 = get_w0_11_000(H_11_000)

# H_11_0D = get_H_11_0D()
# w0_11_0D = get_w0_11_0D(H_11_0D)

# H_11_1D = get_H_11_1D()
# w0_11_1D = get_w0_11_1D(H_11_1D)

# H_11_2D = get_H_11_2D()
# w0_11_2D = get_w0_11_2D(H_11_2D)

# H_11_D = get_H_11_D()
# w0_11_D = get_w0_11_D(H_11_D)

# H_00_D = get_H_00_D()
# w0_00_D = get_w0_00_D(H_00_D)
# -----------------------------------------------
H_10_000 = get_H_10_000()
w0_10_000 = get_w0_10_000(H_10_000)
# H_10_000.print_states()

H_10_0D = get_H_10_0D()
w0_10_0D = get_w0_10_0D(H_10_0D)

H_10_1D = get_H_10_1D()
w0_10_1D = get_w0_10_1D(H_10_1D)

H_10_2D = get_H_10_2D()
w0_10_2D = get_w0_10_2D(H_10_2D)

H_10_D = get_H_10_D()
w0_10_D = get_w0_10_D(H_10_D)

# H_00_D = get_H_00_D()
# w0_00_D = get_w0_00_D(H_00_D)
# -----------------------------------------------
# H_01_000 = get_H_01_000()
# H_01_000.print_states()
# w0_01_000 = get_w0_01_000(H_01_000)

# H_01_0D = get_H_01_0D()
# H_01_0D.print_states()

# w0_01_0D = get_w0_01_0D(H_01_0D)

# H_01_1D = get_H_01_1D()
# w0_01_1D = get_w0_01_1D(H_01_1D)

# H_01_2D = get_H_01_2D()
# w0_01_2D = get_w0_01_2D(H_01_2D)

# H_01_D = get_H_01_D()
# w0_01_D = get_w0_01_D(H_01_D)

# H_00_D = get_H_00_D()
# w0_00_D = get_w0_00_D(H_00_D)
# -----------------------------------------------
# w0_00_D.print()
# print()
# exit(0)
# w0_11_000.print()
# print()

# w0_11_0D.print()
# print()
# w0_11_1D.print()
# print()
# w0_11_2D.print()
# print()

# w0_11_D.print()
# exit(0)
# ---------------------------------------------------------------------------------------------------------------------
folder = 'sink3/0_1ms_01ns_l05g_l05g'
mkdir(folder)
# mkdir('sink/1ms_l001g')
# ---------------------------------------------------------------------------------------------------------------------

for state in [
    # ---------------
    # 0
    {
        'name': '10_000',
        'w0': w0_10_000,
        'H': H_10_000,
    },
    {
        'name': '10_0D',
        'w0': w0_10_0D,
        'H': H_10_0D,
    },
    {
        'name': '10_1D',
        'w0': w0_10_1D,
        'H': H_10_1D,
    },
    {
        'name': '10_2D',
        'w0': w0_10_2D,
        'H': H_10_2D,
    },
    {
        'name': '10_D',
        'w0': w0_10_D,
        'H': H_10_D,
    },
    # ---------------
    # ---------------
    # 1
    # {
    #     'name': '01_000',
    #     'w0': w0_01_000,
    #     'H': H_01_000,
    # },
    # {
    #     'name': '01_0D',
    #     'w0': w0_01_0D,
    #     'H': H_01_0D,
    # },
    # {
    #     'name': '01_1D',
    #     'w0': w0_01_1D,
    #     'H': H_01_1D,
    # },
    # {
    #     'name': '01_2D',
    #     'w0': w0_01_2D,
    #     'H': H_01_2D,
    # },
    # {
    #     'name': '01_D',
    #     'w0': w0_01_D,
    #     'H': H_01_D,
    # },
    # ---------------
    # {
    #     'name': '11_000',
    #     'w0': w0_11_000,
    #     'H': H_11_000,
    # },
    # {
    #     'name': '11_0D',
    #     'w0': w0_11_0D,
    #     'H': H_11_0D,
    # },
    # {
    #     'name': '11_1D',
    #     'w0': w0_11_1D,
    #     'H': H_11_1D,
    # },
    # {
    #     'name': '11_2D',
    #     'w0': w0_11_2D,
    #     'H': H_11_2D,
    # },
    # {
    #     'name': '11_D',
    #     'w0': w0_11_D,
    #     'H': H_11_D,
    # },


    
    # {
    #     'name': '00_D',
    #     'w0': w0_00_D,
    #     'H': H_00_D,
    # },
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
        # 'lindblad': {
        #     'out': {
        #         'L': operator_a3all(state['H']),
        #         'l': l,
        #     },
        # },
        'lindblad': {
            'out': [
                {
                'L': operator_a3all_new(state['H'], ph_type=1),
                'l': l,
                },
                # {
                # 'L': operator_a3all_new(state['H'], ph_type=2),
                # 'l': l,
                # },
            ],
        },
        # 'observe': '_1',
        'observe': '1_',
        'print_all_sink': True,
    })

    pickle_dump(T_list, folder + '/' + 'T_list_' + state['name'] + '.pkl')
    pickle_dump(sink_list, folder + '/' + 'sink_list_' + state['name'] + '.pkl')
    # -----------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------

# =====================================================================================================================
