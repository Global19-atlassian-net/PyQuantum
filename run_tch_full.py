# system
import copy
from PyQuantum.Common.Matrix import *
import itertools
import sys

# TCH
from PyQuantum.TCH_Full.Cavity import Cavity
from PyQuantum.TCH_Full.CavityChain import CavityChain
from PyQuantum.TCH_Full.Hamiltonian import *

from PyQuantum.TCH_Full.WaveFunction import WaveFunction
from PyQuantum.TCH_Full.DensityMatrix import *
from PyQuantum.TCH_Full.FullBase import *

from PyQuantum.TCH_Full.Evolution import *

# Common
from PyQuantum.Common.LoadPackage import *
from PyQuantum.Common.STR import *

from PyQuantum.Common.ext import mkdir
from PyQuantum.Common.Print import *
from PyQuantum.Common.PyPlot import PyPlot3D

# import PyQuantum.TCH_Full.WaveFunction as wf2

# from shutil import copyfile
# from numpy.random import rand

import PyQuantum.TCH_Full.config as config
# config = load_pkg("config", "PyQuantum/TC/config.py")

mkdir(config.path)
# copyfile("PyQuantum/TC/config.py", config.path + '/config.py')

cavity_1 = Cavity(n=config.n_1, wc=config.wc_1, wa=config.wa_1, g=config.g_1)

cavity_1.print(title="Cavity 1:")

cavity_2 = Cavity(n=config.n_2, wc=config.wc_2, wa=config.wa_2, g=config.g_2)

cavity_2.print(title="Cavity 2:")

# cavity_3 = Cavity(n=config.n_2, wc=config.wc_2, wa=config.wa_2, g=config.g_2)

# cavity_3.print(title="Cavity 2:")

cv_chain = CavityChain([cavity_1, cavity_2])

print("T:", config.T)
print("nt:", config.nt)
print("dt:", config.dt)

print()

H = Hamiltonian(capacity=config.capacity,
                cv_chain=cv_chain, mu=config.mu, RWA=True)


# print(np.shape(H))
# print(H.size)
# exit(0)
# print(H[0, 0])
# Hm = Matrix(m=np.shape(H)[0], n=np.shape(H)[1], dtype=np.complex128)
# Hm.data = H
# print(Hm[0])
# for i in range(100):
#     for j in range(100):
#         Hm.data[i, j] = H[i, j]
H.write_to_file(filename=config.H_csv)
# print(np.shape(Hm.data))
# print(Hm.data)
# exit(0)
w0 = WaveFunction(ph_count1=2, init_state1=config.init_state1,
                  ph_count2=2, init_state2=config.init_state2)

Run(w0=w0, H=H, t0=0, t1=config.T, nt=500, initstate1=config.init_state1, initstate2=config.init_state2,
    ph_count1=2, ph_count2=2, config=config, ymin=0, ymax=1, RWA=True, title='title', color='blue')

print(2)
# ph = [[0, 1, 2, 3], [0, 1]]

# ph_base2 = list(itertools.product([0, 1], repeat=1))
# ph_base2 = [list(i) for i in ph_base2]

# ph_chain = [ph_base1, ph_base2]

# AtomicBase = itertools.product(*ph_chain)


# exit(0)


# for i in AtomicBase:
# print(i, np.sum(i))


# for i in range(0, len(cv_chain.cavities)):
#     BASE.append(ph_chain[i])
#     BASE.append(AtomicBase[i])

# print(BASE)

# def get_full_base(cv_chain):
#     BASE = []

#     ph_chain = get_ph_base_chain(cv_chain)
#     AtomicBase = get_at_base_chain(cv_chain)

#     for i in range(np.shape(ph_chain)[0]):
#         for j in range(np.shape(AtomicBase)[0]):
#             b = []

#             ssum = 0
#             # print(ph_chain[i][0], ph_chain[i][1])
#             for cv in range(0, len(cv_chain.cavities)):
#                 ssum += ph_chain[i][cv][0]
#                 ssum += np.sum(AtomicBase[j][cv])

#                 b.append(ph_chain[i][cv][0])
#                 b.append(AtomicBase[j][cv])

#             if ssum > config.capacity:
#                 continue

#             BASE.append(b)

#     for i in BASE:
#         print(i)


# print(ph_chain[i], AtomicBase[j])
# d = np.outer(ph_chain, AtomicBase)

# for i in d:
# print(i)
# exit(0)
# print(np.shape(ph_chain))
# for ph_i in np.shape(0):
#   for ph_j in np.shape(0)
#         for i in AtomicBase:
#             if ph1+ph2+np.sum(i) > config.capacity:
#                 continue
#             # print(i)
#             BASE.append([ph1, i, ph2, i])

# for i in BASE:
#     print(i)
# H = Hamiltonian(capacity=config.capacity, cv_chain=cv_chain)

# H.print_states()

# H.print()

# w_0 = WaveFunction(states=H.states, init_state=config.init_state)

# w_0.print()

# run_wf(w_0=w_0, H=H, dt=config.dt, nt=config.nt,
#        config=config, fidelity_mode=True)


# # -------------------------------------------------------------------------------------------------
# title = r'$RWA$'+'\n'
# color = 'blue'
# # run_RWA(w0=w_0, H=H, t0=0, t1=config.T, nt=config.nt, initstate=config.init_state,
# #         certain_state=config.init_state, ymin=0, ymax=1.005, title=title, color=color)

# # exit(0)

# # -------------------------------------------------------------------------------------------------
# # H_field = H.get_Hfield()
# # H_atoms = H.get_Hatoms()
# # H_int_RWA = H.get_Hint_RWA()


# y_scale = 1

# if config.T < 0.25 * config.mks:
#     y_scale = 0.1
# elif config.T <= 0.5 * config.mks:
#     y_scale = 0.025
# elif config.T == 0.5 * config.mks:
#     y_scale = 0.01
# elif config.T == 1 * config.mks:
#     y_scale = 7.5
#     # y_scale = 10
# elif config.T == 5 * config.mks:
#     y_scale = 1


# if not __debug__ or __debug__:
#     title = ""
#     # title += "<b>"
#     # title += "n = " + str(config.n)
#     # if config.capacity - config.n > 0:
#     #     title += "<br>" + str(config.capacity - config.n) + \
#     #         " фотонов в полости"
#     # # else:
#     # # title += "<br>" + "empty cavity"

#     # # title += "<br>atoms state: |Ψ<sub>0</sub> i = |11...1>A<sub>0</sub> |00...0>A<sub>1</sub> |vaki<sub>p</sub>" + \
#     # #     str(config.init_state)
#     # title += "<br>"
#     # title += "<br>w<sub>c</sub> = " + wc_str(config.wc)
#     # title += "<br>w<sub>a</sub> = " + wa_str(config.wa)
#     # title += "<br> g/hw<sub>c</sub> = " + str(config.g/config.wc)
#     # title += "<br>"
#     # title += "<br>"
#     # title += "</b>"

#     PyPlot3D(
#         title=title,
#         z_csv=config.path + "/" + "z.csv",
#         x_csv=config.path + "/" + "x.csv",
#         y_csv=config.path + "/" + "t.csv",
#         # t_coeff=20000 / 1000 * (config.T / 1e-6),
#         online=False,
#         path=config.path,
#         filename="Bipartite",
#         xaxis="states",
#         yaxis="time, " + T_str_mark(config.T),
#         y_scale=y_scale
#     )
