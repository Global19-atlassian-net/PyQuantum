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
from PyQuantum.TC3_Lindblad.Cavity import Cavity
from PyQuantum.TC3_Lindblad.Hamiltonian import Hamiltonian

from PyQuantum.TC3_Lindblad.WaveFunction import WaveFunction
from PyQuantum.TC3_Lindblad.DensityMatrix import DensityMatrix

from PyQuantum.TC3_Lindblad.Evolution import run_out_click

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
from PyQuantum.Common.Quantum.Operators import operator_a3
# ---------------------------------------------------------------------------------------------------------------------

# BEGIN--------------------------------------------------- MPI4PY -----------------------------------------------------
# mpi4py
from mpi4py import MPI

comm = MPI.COMM_WORLD

mpirank = comm.Get_rank()
mpisize = comm.Get_size()
# END----------------------------------------------------- MPI4PY -----------------------------------------------------

# BEGIN--------------------------------------------------- READ_CFG ---------------------------------------------------
if len(sys.argv) < 2:
    print("No config")
    exit(1)

cfg = load_pkg(sys.argv[1], sys.argv[1])

T = cfg.T
dt = cfg.dt

# nt_batch = cfg.nt_batch

lg = cfg.lg
lg_str = cfg.lg_str

dt_click = cfg.dt_click
dt_click_str = cfg.dt_click_str

out_path = cfg.out_path

precision = cfg.precision
sink_limit = cfg.sink_limit
thres = cfg.thres

epoch = cfg.epoch
epoch_size = cfg.epoch_size

if mpirank == 0:
    mkdir(out_path)
    mkdir(out_path + '/' + lg_str)
    mkdir(out_path + '/' + lg_str + '/' + dt_click_str)
    mkdir(out_path + '/' + lg_str + '/' + dt_click_str + '/' + '11_000')
    mkdir(out_path + '/' + lg_str + '/' + dt_click_str + '/' + '11_D0')

comm.barrier()

out_path = out_path + '/' + lg_str + '/' + dt_click_str
# END----------------------------------------------------- READ_CFG ---------------------------------------------------

# config.capacity = 2
# config.n_atoms = 2

# cavity = Cavity(config.wc, config.wa, config.g, config.n_atoms)

# -----------------------------------------------
l = config.g * cfg.lg

# T = 1 * config.ms

# dt = 0.01 / l
# dt = 10 * config.ns
# dt = 1 * config.ns / 10
nt = int(T/dt)
# dt = (0.001/l)

Assert(dt <= 0.01/l, 'dt > 0.01/l')

# nt = int(T/dt)

if mpirank == 0:
    # ----------------------------------
    # cavity.info()

    cprint('T:', 'green', end='')
    print(time_unit_full(T))

    cprint('dt:', 'green', end='')
    print(time_unit_full(dt))

    cprint('nt:', 'green', end='')
    print(nt)

    hr(50)
    # ----------------------------------
    # cprint('nt_batch:', 'green', end='')
    # print(nt_batch)

    cprint('lg_str:', 'green', end='')
    print(lg_str)

    cprint('dt_click:', 'green', end='')
    print(dt_click)

    cprint('dt_click_str:', 'green', end='')
    print(dt_click_str)

    cprint('out_path:', 'green', end='')
    print(out_path)

    cprint('precision:', 'green', end='')
    print(precision)

    cprint('sink_limit:', 'green', end='')
    print(sink_limit)

    cprint('thres:', 'green', end='')
    print(thres)

    cprint('lg:', 'green', end='')
    print(lg)

    cprint('epoch:', 'green', end='')
    print(epoch)

    cprint('epoch_size:', 'green', end='')
    print(epoch_size)
# -----------------------------------------------

H = Hamiltonian(config.capacity, cavity)

s_2 = WaveFunction(states=H.states, init_state=[1, [0, 1]], amplitude=1./sqrt(2)) - \
    WaveFunction(states=H.states, init_state=[1, [1, 0]], amplitude=1./sqrt(2))

t_0 = WaveFunction(states=H.states, init_state=[1, [0, 0]])
# ---------------------------------------------------------------------------------------------------------------------
# mkdir('sink')
# mkdir('sink/1ms_l001g')

for state in [
    # {
    #     'name': 't0',
    #             'obj': t_0,
    # },
    # {
    #     'name': 's2',
    #     'obj': s_2,
    # },
    {
        'name': '11_000',
        'w0': w0_11_000,
        'H': H_11_000,
    },
]:
    if state['name'] not in cfg.w_0_type:
        continue

    state['w0'].normalize()

    ro_0 = DensityMatrix(state['w0'])

    T_list = []
    sink_list = {'0_1': [], '1_2': []}

    t_click = -1

    T_ = 0

    while True:
        t_click = run_out_click({
            "ro_0": copy(ro_0),
            "H": state['H'],
            "dt": dt,
            # "sink_list": sink_list,
            # "T_list": T_list,
            "precision": precision,
            'sink_limit': sink_limit,
            'time_limit': config.ms,
            "thres": thres,
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
            'dt_click': dt_click,
        })

        T_ += t_click

        if T_ > T:
            break

        T_click.append(t_click)

        # print('\t', time_unit_full(T_))

    fname = out_path + '/' + state['name'] + '/' + \
        str(epoch_size*epoch+mpirank) + '.pkl'
    # fname = out_path + '/' + w_0['name'] + '/'+str(100*1+mpirank) + '.pkl'
    # print(fname)

    pickle_dump(T_click, fname)
# ---------------------------------------------------------------------------------------------------------------------

# =====================================================================================================================
