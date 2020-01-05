# ---------------------------------------------------------------------------------------------------------------------
# sys
import sys
# ---------------------------------------------------------------------------------------------------------------------
# system
from math import sqrt, ceil
# ---------------------------------------------------------------------------------------------------------------------
# scientific
import numpy as np
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.TC_Lindblad
from PyQuantum.TC_Lindblad.Cavity import Cavity
from PyQuantum.TC_Lindblad.Hamiltonian import Hamiltonian

from PyQuantum.TC_Lindblad.WaveFunction import WaveFunction
from PyQuantum.TC_Lindblad.DensityMatrix import DensityMatrix

from PyQuantum.TC_Lindblad.Evolution import run_out_click

import PyQuantum.TC_Lindblad.config as config
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Tools
from PyQuantum.Tools.LoadPackage import load_pkg
from PyQuantum.Tools.Assert import *
from PyQuantum.Tools.Print import hr
from PyQuantum.Tools.MkDir import *
from PyQuantum.Tools.CSV import *
from PyQuantum.Tools.Units import *
from PyQuantum.Tools.Pickle import *
from copy import copy
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Common
from PyQuantum.Common.Quantum.Operators import operator_a, operator_across
# ---------------------------------------------------------------------------------------------------------------------
config.capacity = 1
config.n_atoms = 2

cavity = Cavity(config.wc, config.wa, config.g, config.n_atoms)

# -----------------------------------------------
l = config.g * 0.01

T = 1 * config.ms

# dt = 0.01 / l
dt = 1 * config.ns
# dt = 1 * config.ns / 10
nt = int(T/dt)
# dt = (0.001/l)

# Assert(dt <= 0.01/l, 'dt > 0.01/l')

nt = int(T/dt)

cavity.info()

cprint('T:', 'green', end='')
print(time_unit_full(T))

cprint('dt:', 'green', end='')
# print(time_unit_full(dt))

cprint('nt:', 'green', end='')
print(nt)
# -----------------------------------------------

H = Hamiltonian(config.capacity, cavity)

s_2 = WaveFunction(states=H.states, init_state=[1, [0, 1]], amplitude=1./sqrt(2)) - \
    WaveFunction(states=H.states, init_state=[1, [1, 0]], amplitude=1./sqrt(2))

t_0 = WaveFunction(states=H.states, init_state=[1, [0, 0]])
# ---------------------------------------------------------------------------------------------------------------------
mkdir('sink')
mkdir('sink/1ms_l001g')

for w_0 in [
    {
        'name': 't0',
                'obj': t_0,
    },
    # {
    #     'name': 's2',
    #     'obj': s_2,
    # },
]:
    w_0['obj'].normalize()

    ro_0 = DensityMatrix(w_0['obj'])

    T_list = []
    sink_list = []

    T_click = []

    for nt in range(0, 100):
        t_click = run_out_click({
            "ro_0": copy(ro_0),
            "H": H,
            "dt": dt,
            # "sink_list": sink_list,
            "T_list": T_list,
            "precision": 1e-3,
            'sink_limit': 1,
            'time_limit': config.ms,
            "thres": 0.001,
            'lindblad': {
                'out': {
                    'L': operator_a(H, H.capacity, H.cavity.n_atoms),
                    'l': l
                },
            },
        })
        print(t_click)
        T_click.append(t_click)

    for t in T_click:
        print(time_unit_full(t))
    # MkDir('sink')
    # pickle_dump(T_list, 'sink/1ms_l001g/T_list_' + w_0['name'] + '.pkl')
    # pickle_dump(sink_list, 'sink/1ms_l001g/sink_list_' + w_0['name'] + '.pkl')
    pickle_dump(T_click, 'T_click_' + w_0['name'] + '.pkl')

    # list_to_csv(T_list, 'MM/' + path + '/' + 'T_' + w_0['name'] + '.csv')
    # list_to_csv(np.array(T_list) * 1e9, 'MM/' + path + '/' + 'T_' + w_0['name'] + '.csv')
    # list_to_csv(sink_list, 'MM/' + path + '/' +
    #             'sink_' + w_0['name'] + '.csv')
# ---------------------------------------------------------------------------------------------------------------------

# =====================================================================================================================
