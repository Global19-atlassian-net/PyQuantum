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
# mpi4py
from mpi4py import MPI

comm = MPI.COMM_WORLD

mpirank = comm.Get_rank()
mpisize = comm.Get_size()
# ---------------------------------------------------------------------------------------------------------------------


# BEGIN--------------------------------------------------- CONFIG_IMPORT ----------------------------------------------
Assert(len(sys.argv) > 1, 'len(sys.argv) == 1', FILE(), LINE())
config_path = sys.argv[1]
config = load_pkg(config_path, config_path)

g_list = config.g_list
g_list = np.round(g_list, 4)

l_list = config.l_list
l_list = np.round(l_list, 2)

sink_threshold = config.sink_threshold
# END----------------------------------------------------- CONFIG_IMPORT ----------------------------------------------


g_count = len(g_list)
g_per_node = ceil(g_count / mpisize)

if mpirank == mpisize-1:
    my_g = g_count - (mpisize-1) * g_per_node
    my_g_list = g_list[(mpisize-1) * g_per_node:]
    print('My rank is ', mpirank, '/', mpisize, ' ', my_g, ' [', (mpisize-1) * g_per_node, ', :] ', my_g_list, sep='')
else:
    my_g = g_per_node
    my_g_list = g_list[(mpirank) * g_per_node:(mpirank+1) * g_per_node]
    # print('My rank is ', mpirank, '/', mpisize, ' ', my_g,
    #       ' [', (mpirank) * g_per_node, ',', (mpirank+1) * g_per_node, '] ', my_g_list, sep='')


my_g_list = np.round(my_g_list, 4)

state_type = config.state_type

# ---------------------------------------------------
# mkdir
# outdir = 'sink_out' + '/' + str(np.round(1 - sink_threshold, 3)) + '/' + state_type
outdir = config.outdir

if mpirank == 0:
    print('start done')
    print(outdir)
    mkdir(outdir)
    print('done')

comm.Barrier()
# ---------------------------------------------------

for g_coeff in my_g_list:
    g = g_coeff * config.wc

    # print('-' * 100)
    # print('g:', g)
    # print()

    for l_coeff in l_list:
        l = g * l_coeff

        # print('\tl:', l)

        cavity = Cavity(config.wc, config.wa, g, config.n_atoms)

        H = Hamiltonian(config.capacity, cavity)

        if state_type == 't_0':
            w_0 = WaveFunction(states=H.states, init_state=[1, [0, 0]])
        elif state_type == 's_2':
            w_0 = WaveFunction(states=H.states, init_state=[1, [0, 1]], amplitude=1./sqrt(2)) - \
                WaveFunction(states=H.states, init_state=[1, [1, 0]], amplitude=1./sqrt(2))
        else:
            Assert(0 == 1, 'undefined state type', FILE(), LINE())

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
        list_to_csv(z_data_g, outdir + '/t_' + str(g_coeff) + '_' + str(l_coeff) + '.csv')

        list_to_csv(T_list, outdir + '/time_' + str(g_coeff) + '_' + str(l_coeff) + '.csv')

        list_to_csv(np.round(sink_list, 3), outdir + '/sink_' + str(g_coeff) + '_' + str(l_coeff) + '.csv')
        # -------------------------------------------------------------------------------------------------------------

# =====================================================================================================================
# print('\t', w_0['name'], ': time = ', T_list[-1], sep='')
# list_to_csv(z_data_g['s_2'], outdir + '/s_2/t_' + str(g) + '_' + str(l) + '.csv')
# print()

# print('-' * 100)
# print()

# list_to_csv(z_data_g['s_2'], outdir + '/s_2/t_' + str(g) + '.csv')

# if mpirank == 0:
#     list_to_csv([g_list], outdir + '/t_0/g.csv')
#     # list_to_csv([g_list], outdir + '/s_2/g.csv')

#     list_to_csv([l_list], outdir + '/t_0/l.csv')
# list_to_csv([l_list], outdir + '/s_2/l.csv')


# print()
# print('len =', )
# 100 / 3
# 33 33 34
# 34 34 32
# l_list = np.round(l_list, 2)

# # print('g_list:', g_list)
# # print('l_list:', l_list)

# # exit(0)

# x_data = g_list  # g
# y_data = l_list  # l
# z_data = {'t_0': [], 's_2': []}  # t
# =====================================================================================================================
# g_list = np.arange(0.01, 0.05, 0.01) * 1e-2
# g_list = np.arange(0.01, 1.01, 0.01) * 1e-2
# l_list = list(np.arange(0.01, 0.51, 0.01))
# l_list = list(np.arange(0.51, 1.01, 0.01))
# l_list = list(np.arange(0.01, 1.01, 0.01))
# l_list = list(np.arange(0.01, 1.01, 0.01))
# l_list = list(np.arange(0.51, 1.01, 0.01))
# l_list = list(np.arange(0.50, 1.01, 0.01))
# l_list = list(np.arange(0.01, 1.01, 0.01)) + list(np.arange(1, 100.5, 1.0))
# l_list = list(np.arange(1.1, 1.2, 0.1))
# l_list = list(np.arange(1.1, 10.1, 0.1))

# # g_list = np.arange(0.01, 0.03, 0.01) * 1e-2
# g_list = np.arange(0.01, 0.11, 0.01) * 1e-2
# l_list = list(np.arange(0.01, 0.03, 0.01))
# =====================================================================================================================
# 0.001
# l_threshold = 0.005
# l_threshold = 0.01
# l_threshold = 0.05
# l_threshold = 0.1
# =====================================================================================================================
