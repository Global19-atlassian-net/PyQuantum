# ---------------------------------------------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
# ---------------------------------------------------------------------------------------------------------------------
from PyQuantum.TC_Lindblad.Cavity import Cavity
from PyQuantum.TC_Lindblad.Hamiltonian import Hamiltonian

from PyQuantum.TC_Lindblad.WaveFunction import WaveFunction
from PyQuantum.TC_Lindblad.DensityMatrix import DensityMatrix

from PyQuantum.TC_Lindblad.Evolution import run, run2

from PyQuantum.Tools.Print import hr
from PyQuantum.Common.STR import *
from PyQuantum.Common.Quantum.Fidelity import *
from PyQuantum.Common.Quantum.Operators import operator_a, operator_across, operator_acrossa, operator_aacross

import scipy.sparse.linalg as lg
import PyQuantum.TC_Lindblad.config as config
from PyQuantum.Tools.CSV import *

# ---------------------------------------------------------------------------------------------------------------------
n_states = 100

_a = []

for i in range(n_states):
    A = np.random.rand(2, 2)
    A_comp = A.view(dtype=np.complex128)

    _a.append(A_comp)

# for i in _a:
#     print(i)
# exit(0)
# singlet
config.capacity = 3
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

_a = [
    {
        'name': 's_2',
        'ampl': [1, 0],
    },
    {
        'name': 't_0',
        'ampl': [0, 1],
    },
]

k = 0

for i in _a:
    hr(100)
    # print(i[0][0])
    # w_0 = s_2 * i[0][0]
    w_0 = s_2 * i['ampl'][0] + t_0 * i['ampl'][1]
    # w_0 = s_2 * i[0][0] + t_0 * i[1][0]
    w_0.normalize()

    d = {}

    d['fidelity_t0'] = [Fidelity_full(w_0, t_0)]
    d['fidelity_s2'] = [Fidelity_full(w_0, s_2)]

    ro_t = ro_0 = DensityMatrix(w_0)

    time = 0

    T_list = []
    sink_list = []

    cnt = run2({
        "ro_0": ro_t,
        "H": H,
        "T": config.T,
        "dt": config.dt,
        "nt": config.nt,
        "thres": 0.1,
        "sink_list": sink_list,
        "T_list": T_list,
        "precision": 1e-4,
        'sink_limit': 1,
        'time_limit': 100*config.mks,
        'in_photons': 1,
        'lindblad': {
            'in': {
                'L': operator_across(H, H.capacity, H.cavity.n_atoms),
                'l': config.l
            },
            'out': {
                'L': operator_a(H, H.capacity, H.cavity.n_atoms),
                'l': config.l
            }
        },
    })

    print("cnt =", cnt)
    print("fidelity_t0 =", d['fidelity_t0'])
    print("fidelity_s2 =", d['fidelity_s2'])
    hr(100)
    hr(0)

    d['cnt'] = [cnt]
    d['T_list'] = T_list

    for params in ['cnt', 'T_list', 'fidelity_t0', 'fidelity_s2']:
        print(d)
        list_to_csv(d[params], 'out_2/' + params + str(k) + '.csv')
    # list_to_csv(d['fidelity_s2'], 'oout/fidelity_s2' + str(k) + '.csv')
    # list_to_csv([d['cnt']], 'oout/cnt' + str(k) + '.csv')
    # list_to_csv(d['T_list'], 'oout/T_list_' + str(k) + '.csv')
    k += 1
    # result.append(d)

    # print(result)
    # exit(0)
    # exit(0)


# for k, v in enumerate(result):
#     list_to_csv(v['fidelity_t0'], 'oout/fidelity_t0' + str(k) + '.csv')
#     list_to_csv(v['fidelity_s2'], 'oout/fidelity_s2' + str(k) + '.csv')
#     list_to_csv([v['cnt']], 'oout/cnt' + str(k) + '.csv')
#     list_to_csv(v['T_list'], 'oout/T_list_' + str(k) + '.csv')
# fidelity_t0_list = []
# fidelity_s2_list = []
# cnt_list = []

# # max_sch = 0
# for i in result:
#     fidelity_t0_list.append(i['fidelity_t0'])
#     fidelity_s2_list.append(i['fidelity_s2'])

#     cnt_list.append(i['cnt'])
#     # print(i['cnt'], i['fidelity'])

#     # max_sch = max(max_sch, i['cnt'])

# list_to_csv(fidelity_t0_list, 'rand_fidelity_t0_list.csv')
# list_to_csv(fidelity_s2_list, 'rand_fidelity_s2_list.csv')

# list_to_csv(cnt_list, 'rand_cnt_list.csv')
# list_to_csv(sink_list, 'rand_sink_list.csv')

# plt.xlim(0, max_sch)
# plt.ylim(0, 1)
# plt.plot(cnt_list, fidelity_list, 'ro')
# plt.show()

# plt.xlim(0, max_sch)
# plt.ylim(0, 1)
# plt.plot(cnt_list, fidelity_0_list, 'ro')
# plt.show()

exit(0)
# s_2 = WaveFunction(states=H.states, init_state=[0, [0, 1]], amplitude=1./sqrt(2)) - \
#     WaveFunction(states=H.states, init_state=[0, [1, 0]], amplitude=1./sqrt(2))

# t_0 = WaveFunction(states=H.states, init_state=[0, [0, 0]])
# s_2.print()

ro_0 = DensityMatrix(s_2)

# print()

# t_0 = WaveFunction(states=H.states, init_state=[0, [0, 0]])

# ro_0 = DensityMatrix(t_0)
time = 0

T_list = []
sink_list = []

ro_t = ro_0

cnt = 0

cnt = run2({
    "ro_0": DensityMatrix(t_0),
    "H": H,
    "T": config.T,
    "dt": config.dt,
    "nt": config.nt,
    "thres": 0.1,
    "sink_list": sink_list,
    "T_list": T_list,
    "precision": 1e-3,
    'sink_limit': 1,
    'time_limit': config.mks,
    'in_photons': 1,
    'lindblad': {
        'in': {
            'L': operator_across(H, H.capacity, H.cavity.n_atoms),
            'l': config.l
        },
        'out': {
            'L': operator_a(H, H.capacity, H.cavity.n_atoms),
            'l': config.l
        }
    },
})

print("cnt =", cnt)
exit(0)
# ---------------------------------------------------------------------------------------------------------------------


# run({
#     "ro_0": ro_t,
#     "H": H,
#     "T": config.T,
#     "dt": config.dt,
#     "nt": config.nt,
#     "thres": 0.1,
#     # "x_csv": config.x_csv,
#     # "y_csv": config.y_csv,
#     # "z_csv": config.z_csv,
#     "sink_list": sink_list,
#     "T_list": T_list,
#     "precision": 1e-3,
#     'sink_limit': 1,
#     'lindblad': [
#         {
#             'L': operator_a(H, H.capacity, H.cavity.n_atoms),
#             'l': config.l
#         }
#     ],
# })
# exit(0)


# while time < 1:
#     # while time < 10 * config.ms:
#     # ---------------------------------------------------------
#     run({
#         "ro_0": ro_t,
#         "H": H,
#         "T": config.T,
#         "dt": config.dt,
#         "nt": config.nt,
#         "thres": 0.1,
#         # "x_csv": config.x_csv,
#         # "y_csv": config.y_csv,
#         # "z_csv": config.z_csv,
#         # "sink_list": sink_list,
#         "T_list": T_list,
#         "precision": 1e-3,
#         # 'sink_limit': 1,
#         'in_photons': 1,
#         'lindblad': [
#             {
#                 'L': operator_across(H, H.capacity, H.cavity.n_atoms),
#                 'l': config.l
#             }
#         ],
#     })

#     time += T_list[-1]

#     print("time_2: ", time, ' s', sep='')
#     print(T_list[-1])
#     # exit(0)
#     # ---------------------------------------------------------
#     diag_abs = np.abs(ro_t.data.diagonal(), dtype=np.longdouble)
#     energy = ro_t.energy(H.capacity, H.cavity.n_atoms, H.states_bin, diag_abs)
#     print("energy:", np.sum(energy))
#     # print(diag_abs)
#     # exit(0)
#     ret = run({
#         "ro_0": ro_t,
#         "H": H,
#         "T": config.T,
#         "dt": config.dt,
#         "nt": config.nt,
#         "thres": 0.1,
#         # "x_csv": config.x_csv,
#         # "y_csv": config.y_csv,
#         # "z_csv": config.z_csv,
#         "sink_list": sink_list,
#         "T_list": T_list,
#         "precision": 1e-3,
#         'sink_limit': 1,
#         'en_': 2,
#         'lindblad': [
#             {
#                 'L': operator_a(H, H.capacity, H.cavity.n_atoms),
#                 'l': config.l
#             }
#         ],
#     })

#     time += T_list[-1]
#     # print(time, config.dt, T_list[-1])
#     # exit(0)
#     print("time_1: ", time, ' s', sep='')
#     # print(T_list[-1], sink_list[-1])
#     if ret:
#         cnt += 1
#     # ---------------------------------------------------------
#     print()


# print("cnt:", cnt)

# exit(0)

# -------------------------
sink_list = []
T_list = []

time_2 = run({
    "ro_0": ro_0,
    "H": H,
    "T": config.T,
    "dt": config.dt,
    "nt": config.nt,
    "thres": 0.1,
    # "x_csv": config.x_csv,
    # "y_csv": config.y_csv,
    # "z_csv": config.z_csv,
    "sink_list": sink_list,
    "T_list": T_list,
    "precision": 1e-3,
    'sink_limit': 1,
    'lindblad':
        {
            'L': operator_acrossa(H, H.capacity, H.cavity.n_atoms),
            'l': config.l
        },
})

# for i in sink_list:
#     print(i)

# print(T_list[-1])

# time_2 = run({
#     "ro_0": ro_0,
#     "H": H,
#     "T": config.T,
#     "dt": config.dt,
#     "nt": config.nt,
#     "thres": 0.1,
#     # "x_csv": config.x_csv,
#     # "y_csv": config.y_csv,
#     # "z_csv": config.z_csv,
#     # "sink_list": sink_list,
#     "T_list": T_list,
#     "precision": 1e-3,
#     # 'sink_limit': 1,
#     'en_': 2,
#     'in_photons': 1,
#     'lindblad': [
#         {
#             'L': operator_across(H, H.capacity, H.cavity.n_atoms),
#             'l': config.l
#         }
#     ],
# })

# for i in sink_list:
#     print(i)

# print(T_list[-1])

# # plt.ylim(0, 1)
# # plt.plot(T_list, sink_list)
# # plt.show()
# # -------------------------
# exit(0)


# ---------------------------------------------------------------------------------------------------------------------
# H = Hamiltonian(1, cavity)

t_0 = WaveFunction(states=H.states, init_state=[1, [0, 0]])

ro_0 = DensityMatrix(t_0)

t_0.print()

print()
# ---------------------------------------------------------------------------------------------------------------------
# -------------------------
# sink_list = []
T_list = []

time_0 = run({
    "ro_0": ro_0,
    "H": H,
    "T": config.T,
    "dt": config.dt,
    "nt": config.nt,
    "l": config.l,
    "thres": 0.1,
    # "x_csv": config.x_csv,
    # "y_csv": config.y_csv,
    # "z_csv": config.z_csv,
    "sink_list": sink_list,
    "T_list": T_list,
    "precision": 1e-3,
    'sink_limit': 2,
    'en_': 1,
}, check=True)
# }, check=False)

plt.ylim(0, 1)
plt.plot(T_list, sink_list)
plt.show()
# -------------------------

# }, check=True)

# ro_0.print()

# print("t_2:", t_2)
# print("time_0:", time_0)

# plt.plot(x, y)
# plt.show()
# sink_list = []
# plt.ylim(0, config.capacity)
# plt.ylim(0, 1)
# plt.plot(T_list, sink_list)
# plt.show()

# for i in sink_list:
#     print(i)

# plt.ylim(0, 1)
# plt.plot(T_list, sink_list)
# plt.show()

# cavity = Cavity(config.wc, config.wa, config.g, config.n_atoms)

# H.print()
t()
