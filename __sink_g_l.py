# ---------------------------------------------------------------------------------------------------------------------
# system
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
# PyQuantum.Common
from PyQuantum.Common.Quantum.Operators import operator_a, operator_across
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Tools
from PyQuantum.Tools.Print import hr
from PyQuantum.Tools.CSV import *
from PyQuantum.Tools.MkDir import *
# ---------------------------------------------------------------------------------------------------------------------
# import mpi4py

from mpi4py import MPI

comm = MPI.COMM_WORLD

mpirank = comm.Get_rank()
mpisize = comm.Get_size()

print('My rank is ', mpirank, mpisize)

# exit(0)


# config.capacity = 2
# config.n_atoms = 2

# # g_list = np.arange(0.01, 0.03, 0.01) * 1e-2
# g_list = np.arange(0.01, 0.11, 0.01) * 1e-2
# # g_list = np.arange(0.01, 1.01, 0.01) * 1e-2
# # l_list = list(np.arange(0.01, 0.03, 0.01))
# l_list = list(np.arange(0.01, 1.01, 0.01)) + list(np.arange(1, 100.5, 1.0))
# l_list = np.round(l_list, 2)

# # print('g_list:', g_list)
# # print('l_list:', l_list)

# # exit(0)

# x_data = g_list  # g
# y_data = l_list  # l
# z_data = {'t_0': [], 's_2': []}  # t

# mkdir('sink_l_g/t_0/')
# mkdir('sink_l_g/s_2/')

# for g in g_list:
#     print('-' * 100)
#     print('g:', g)
#     print()

#     z_data_g = {'t_0': [], 's_2': []}

#     for l in l_list:
#         config.g = g * config.wc
#         config.l = config.g * l

#         print('\tl:', l)

#         cavity = Cavity(config.wc, config.wa, config.g, config.n_atoms)

#         H = Hamiltonian(config.capacity, cavity)

#         s_2 = WaveFunction(states=H.states, init_state=[1, [0, 1]], amplitude=1./sqrt(2)) - \
#             WaveFunction(states=H.states, init_state=[1, [1, 0]], amplitude=1./sqrt(2))

#         t_0 = WaveFunction(states=H.states, init_state=[1, [0, 0]])

#         config.dt = (0.01 / config.l)
#         # config.dt = (1e-4 / config.g)

#         for w_0 in [{
#                     'name': 's_2',
#                     'obj': s_2,
#                     },
#                     {
#                     'name': 't_0',
#                     'obj': t_0,
#                     }]:
#             ro_0 = DensityMatrix(w_0['obj'])

#             T_list = []
#             sink_list = []

#             run({
#                 "ro_0": ro_0,
#                 "H": H,
#                 "dt": config.dt,
#                 "sink_list": sink_list,
#                 "T_list": T_list,
#                 "precision": 1e-3,
#                 'sink_limit': 1,
#                 'lindblad': {
#                     'out': {
#                         'L': operator_a(H, H.capacity, H.cavity.n_atoms),
#                         'l': config.l
#                     },
#                 },
#             })

#             print('\t', w_0['name'], ': time = ', T_list[-1], sep='')

#             z_data_g[w_0['name']].append(T_list[-1])

#         print()

#     print('-' * 100)
#     print()

#     list_to_csv(z_data_g['t_0'], 'sink_l_g/t_0/t_' + str(g) + '.csv')
#     list_to_csv(z_data_g['s_2'], 'sink_l_g/s_2/t_' + str(g) + '.csv')

#     # z_data['t_0'].append(z_data_g['t_0'])
#     # z_data['s_2'].append(z_data_g['s_2'])

#     # print(z_data_g)

# list_to_csv([x_data], 'sink_l_g/t_0/g.csv')
# list_to_csv([x_data], 'sink_l_g/s_2/g.csv')

# list_to_csv([y_data], 'sink_l_g/t_0/l.csv')
# list_to_csv([y_data], 'sink_l_g/s_2/l.csv')


# list_to_csv(z_data['t_0'], 'sink_l_g/t_0/t.csv')
# list_to_csv(z_data['s_2'], 'sink_l_g/s_2/t.csv')
