# ---------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
# ---------------------------------------------------------------------------------------------------------------------
from PyQuantum.TC_Lindblad.Cavity import Cavity
from PyQuantum.TC_Lindblad.Hamiltonian import Hamiltonian

from PyQuantum.TC_Lindblad.WaveFunction import WaveFunction
from PyQuantum.TC_Lindblad.DensityMatrix import DensityMatrix

from PyQuantum.TC_Lindblad.Evolution import run, run_in_out

from PyQuantum.Tools.Print import hr
from PyQuantum.Common.STR import *
from PyQuantum.Common.Quantum.Fidelity import *
from PyQuantum.Common.Quantum.Operators import operator_a, operator_across, operator_acrossa, operator_aacross

import scipy.sparse.linalg as lg
import PyQuantum.TC_Lindblad.config as config
from PyQuantum.Tools.CSV import *
from PyQuantum.Tools.Units import *
from PyQuantum.Tools.Pickle import *

# ---------------------------------------------------------------------------------------------------------------------
# n_states = 100

# _a = []

# for i in range(n_states):
#     A = np.random.rand(2, 2)
#     A_comp = A.view(dtype=np.complex128)

#     _a.append(A_comp)

# for i in _a:
#     print(i)
# exit(0)
# singlet
config.capacity = 2
config.n_atoms = 2

cavity = Cavity(config.wc, config.wa, config.g, config.n_atoms)

H = Hamiltonian(config.capacity, cavity)

s_2 = WaveFunction(states=H.states, init_state=[0, [0, 1]], amplitude=1./sqrt(2)) - \
    WaveFunction(states=H.states, init_state=[0, [1, 0]], amplitude=1./sqrt(2))
ro_2 = DensityMatrix(s_2)

t_0 = WaveFunction(states=H.states, init_state=[0, [0, 0]])
ro_0 = DensityMatrix(t_0)

# ro_2_sqrt = ro_2.data.sqrt()
# ro_2_sqrt = lg.fractional_matrix_power(ro_2.data, 0.5)

# ro_2.print()
# print(ro_2.abs_trace())
# exit(0)

# print(Fidelity_full(s_2, t_0))
# exit(0)

result = []

# m = 100

# for i in _a:
#     hr(100)
#     # print(i[0][0])
#     # w_0 = s_2 * i[0][0]
#     w_0 = s_2 * i[0][0] + t_0 * i[1][0]
#     w_0.normalize()

#     d = {}
#     # s_2.print()
#     d['fidelity'] = Fidelity_full(w_0, s_2)
#     print(d['fidelity'])

#     m = min(m, d['fidelity'])

# print(m)
# exit(0)

states = [
    # {
    #     'name': 's_2',
    #     'ampl': [1, 0],
    # },
    {
        'name': 't_0',
        'ampl': [0, 1],
    },
]

k = 0

l = 0.1 * config.g

T = 1 * config.ms

dt = 10 * config.ns
nt = int(T/dt)
# dt = (0.001/l)

# Assert(dt <= 0.01/l, 'dt > 0.01/l')

nt = int(T/dt)

cavity.info()

cprint('T:', 'green', end='')
print(time_unit_full(T))

cprint('dt:', 'green', end='')
print(time_unit_full(dt))

cprint('nt:', 'green', end='')
print(nt)

s_2 = WaveFunction(states=H.states, init_state=[0, [0, 1]], amplitude=1./sqrt(2)) - \
    WaveFunction(states=H.states, init_state=[0, [1, 0]], amplitude=1./sqrt(2))

t_0 = WaveFunction(states=H.states, init_state=[0, [0, 0]])

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

    out_data = {}

    time = 0

    T_list = []
    sink_list = []

    cnt = run_in_out({
        "ro_0": ro_0,
        "H": H,
        "T": T,
        "dt": dt,
        "nt": nt,
        "thres": 0.01,
        "sink_list": sink_list,
        "T_list": T_list,
        "precision": 1e-3,
        'sink_limit': 1,
        'time_limit': T,
        'in_photons': 1,
        'lindblad': {
            'in': {
                'L': operator_across(H, H.capacity, H.cavity.n_atoms),
                'l': l
            },
            'out': {
                'L': operator_a(H, H.capacity, H.cavity.n_atoms),
                'l': l
            }
        },
    })

    print("cnt =", cnt)
    hr(100)
    hr(0)

    out_data['cnt'] = [cnt]
    out_data['T_list'] = T_list

    for params in ['cnt', 'T_list']:
        print(out_data)

    pickle_dump(T_list, 'dt_' + w_0['name'] + '_1ms_l01g.pkl')

    # list_to_csv(out_data[params], 'out_2/' + params + str(k) + '.csv')

    k += 1

# =====================================================================================================================
