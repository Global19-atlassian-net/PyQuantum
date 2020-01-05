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
# from PyQuantum.Tools.CSV import *
# from PyQuantum.Tools.Units import *
from PyQuantum.Tools.Hz import *
from PyQuantum.Tools.Pickle import *
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Common
from PyQuantum.Common.Quantum.Operators import operator_a
# ---------------------------------------------------------------------------------------------------------------------
config.capacity = 2
config.n_atoms = 2

g_list = np.arange(0.01, 0.02, 0.01) * 1e-2
l_list = np.arange(1.1, 1.2, 0.1)

sink_threshold = config.sink_threshold

state_type = config.state_type
# ---------------------------------------------------
# mkdir
out_dir = 'sink_single_out'
mkdir(out_dir)

out_dir += '/' + str(np.round(1 - sink_threshold, 3))
mkdir(out_dir)

out_dir += '/' + state_type
mkdir(out_dir)
# ---------------------------------------------------
for g_coeff in g_list:
    g = g_coeff * config.wc

    print('-' * 100)
    print('g_coeff:', g_coeff)
    print('g:', to_Hz(g))
    print()

    for l_coeff in l_list:
        l = g * l_coeff

        print('\tl_coeff:', l_coeff)
        print('\tl:', to_Hz(l))
        print()

        cavity = Cavity(config.wc, config.wa, g, config.n_atoms)

        # print(type(cavity))
        cavity.info()
        # exit(0)
        H = Hamiltonian(config.capacity, cavity)

        if state_type == 't_0':
            w_0 = WaveFunction(states=H.states, init_state=[1, [0, 0]])
        elif state_type == 's_2':
            w_0 = WaveFunction(states=H.states, init_state=[1, [0, 1]], amplitude=1./sqrt(2)) - \
                WaveFunction(states=H.states, init_state=[
                             1, [1, 0]], amplitude=1./sqrt(2))
        else:
            Assert(0 == 1, 'undefined state type')

        config_dt = (0.01 / l)

        z_data_g = []

        ro_0 = DensityMatrix(w_0)

        T_list = []
        sink_list = []

        run({
            "ro_0": ro_0,
            "H": H,
            "dt": config_dt,
            "sink_list": sink_list,
            "T_list": T_list,
            "precision": sink_threshold,
            'sink_limit': 1,
            'lindblad': {
                'out': {
                    'L': operator_a(H, H.capacity, H.cavity.n_atoms),
                    'l': l
                },
            },
        })

        z_data_g.append(T_list[-1])

        # -------------------------------------------------------------------------------------------------------------
        pickle_dump(z_data_g, out_dir + '/t_' + str(g_coeff) +
                    '_' + str(l_coeff) + '.pkl.gz')
        # list_to_csv(z_data_g, out_dir + '/t_' +
        # str(g_coeff) + '_' + str(l_coeff) + '.csv')

        pickle_dump(T_list, out_dir + '/time_' + str(g_coeff) +
                    '_' + str(l_coeff) + '.pkl.gz')
        # list_to_csv(T_list, out_dir + '/time_' +
        # str(g_coeff) + '_' + str(l_coeff) + '.csv')

        pickle_dump(np.round(sink_list, 3), out_dir + '/sink_' +
                    str(g_coeff) + '_' + str(l_coeff) + '.pkl.gz')
        # list_to_csv(np.round(sink_list, 3), out_dir + '/sink_' +
        # str(g_coeff) + '_' + str(l_coeff) + '.csv')
        # -------------------------------------------------------------------------------------------------------------

    print('-' * 100)
    print()
# ---------------------------------------------------------------------------------------------------------------------

# for coeff in np.arange(4.00, 6.01, 1.00):
#     config.l = config.g * coeff
#     config.dt = (0.01/config.l)

#     path = 'M_' + str(np.round(coeff, 3))
#     print(path)
#     mkdir('MM/'+path)

#     for w_0 in [
#         {
#             'name': 't_0',
#             'obj': t_0,
#         },
#         # {
#         #     'name': 's_2',
#         #     'obj': s_2,
#         # },
#     ]:
#         ro_0 = DensityMatrix(w_0['obj'])

#         T_list = []
#         sink_list = []

#         run({
#             "ro_0": ro_0,
#             "H": H,
#             "dt": config.dt,
#             "sink_list": sink_list,
#             "T_list": T_list,
#             "precision": 1e-3,
#             'sink_limit': 1,
#             'lindblad': {
#                 'out': {
#                     'L': operator_a(H, H.capacity, H.cavity.n_atoms),
#                     'l': config.l
#                 },
#             },
#         })

#         list_to_csv(T_list, 'MM/' + path + '/' + 'T_' + w_0['name'] + '.csv')
#         # list_to_csv(np.array(T_list) * 1e9, 'MM/' + path + '/' + 'T_' + w_0['name'] + '.csv')
#         list_to_csv(sink_list, 'MM/' + path + '/' + 'sink_' + w_0['name'] + '.csv')
# # ---------------------------------------------------------------------------------------------------------------------

# =====================================================================================================================
