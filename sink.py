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

from PyQuantum.TC_Lindblad.Evolution import run

import PyQuantum.TC_Lindblad.config as config
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Tools
from PyQuantum.Tools.LoadPackage import load_pkg
from PyQuantum.Tools.Assert import *
from PyQuantum.Tools.Print import hr
from PyQuantum.Tools.MkDir import *
from PyQuantum.Tools.CSV import *
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Common
from PyQuantum.Common.Quantum.Operators import operator_a
# ---------------------------------------------------------------------------------------------------------------------
config.capacity = 2
config.n_atoms = 2

cavity = Cavity(config.wc, config.wa, config.g, config.n_atoms)

cavity.info()

H = Hamiltonian(config.capacity, cavity)

s_2 = WaveFunction(states=H.states, init_state=[1, [0, 1]], amplitude=1./sqrt(2)) - \
    WaveFunction(states=H.states, init_state=[1, [1, 0]], amplitude=1./sqrt(2))

t_0 = WaveFunction(states=H.states, init_state=[1, [0, 0]])
# ---------------------------------------------------------------------------------------------------------------------
for coeff in np.arange(4.00, 6.01, 1.00):
    config.l = config.g * coeff
    config.dt = (0.01/config.l)

    path = 'M_' + str(np.round(coeff, 3))
    print(path)
    mkdir('MM/'+path)

    for w_0 in [
        {
            'name': 't_0',
            'obj': t_0,
        },
        # {
        #     'name': 's_2',
        #     'obj': s_2,
        # },
    ]:
        ro_0 = DensityMatrix(w_0['obj'])

        T_list = []
        sink_list = []

        run({
            "ro_0": ro_0,
            "H": H,
            "dt": config.dt,
            "sink_list": sink_list,
            "T_list": T_list,
            "precision": 1e-3,
            'sink_limit': 1,
            'lindblad': {
                'out': {
                    'L': operator_a(H, H.capacity, H.cavity.n_atoms),
                    'l': config.l
                },
            },
        })

        list_to_csv(T_list, 'MM/' + path + '/' + 'T_' + w_0['name'] + '.csv')
        # list_to_csv(np.array(T_list) * 1e9, 'MM/' + path + '/' + 'T_' + w_0['name'] + '.csv')
        list_to_csv(sink_list, 'MM/' + path + '/' + 'sink_' + w_0['name'] + '.csv')
# ---------------------------------------------------------------------------------------------------------------------

# =====================================================================================================================
