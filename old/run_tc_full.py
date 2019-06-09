# -------------------------------------------------------------------------------------------------
# system
import sys
# -------------------------------------------------------------------------------------------------
# TC
from PyQuantum.TC_Full.Cavity import Cavity
from PyQuantum.TC_Full.Hamiltonian import *

from PyQuantum.TC_Full.WaveFunction import *
from PyQuantum.TC_Full.DensityMatrix import *

from PyQuantum.TC_Full.Evolution import *
# -------------------------------------------------------------------------------------------------
# Common
from PyQuantum.Common.LoadPackage import *
from PyQuantum.Common.STR import *

from PyQuantum.Common.Tools import mkdir
from PyQuantum.Common.Print import *
from PyQuantum.Common.PyPlot import PyPlot3D
# from shutil import copyfile
# from numpy.random import rand
# -------------------------------------------------------------------------------------------------
config = load_pkg("config", "PyQuantum/TC_Full/config.py")

mkdir(config.path)
# copyfile("PyQuantum/TC/config.py", config.path + '/config.py')
# -------------------------------------------------------------------------------------------------
cavity = Cavity(n=config.n, wc=config.wc, wa=config.wa, g=config.g)

print("Cavity:", color="green")

print()

cavity.print_n()
cavity.print_wc()
cavity.print_wa()
cavity.print_g()

print("T:", config.T)
print("nt:", config.nt)
print("dt:", config.dt)

print()

# atomic_base = AtomicBasis(count=config.capacity)

# base = Base(capacity=config.capacity, atomic_base=atomic_base)
# base.print()

# print(len(base.base))

# exit(0)
# -------------------------------------------------------------------------------------------------
H = Hamiltonian(capacity=config.capacity, at_count=config.n,
                wc=config.wc, wa=config.wa, g=config.g, RWA=True)
# H = Hamiltonian(capacity=config.capacity, cavity=cavity)

w0 = get_w0(ph_count=config.capacity, init_state=config.init_state)

title = ''
color = 'blue'

run_RWA(w0=w0, H=H, t0=0, t1=config.T, nt=500, initstate=config.init_state,
        certain_state=config.certain_state, ymin=0, ymax=1.005, title=title, color=color)

# H.print_states()
# H.print()

# exit(0)

# if __debug__:
#     print("Hamiltonian states:", color="green")
#     # H.print()
#     print()

#     H.print_states()

#     H.write_to_file(filename=config.H_csv)
# H.print_html(filename=H_html)
# -------------------------------------------------------------------------------------------------
# w_0 = WaveFunction(ph_count=config.capacity, init_state=config.init_state)
# print(config.init_state)
# w_0 = WaveFunction(states=H.states, init_state=config.init_state) - \
#     WaveFunction(states=H.states, init_state=config.init_state2)

# # print(w_0)
# w_0.normalize()
# w_0.print()

# # exit(0)

# if __debug__:
#     print("Wave Function:", color="green")

#     print()

#     w_0.print()
# # -------------------------------------------------------------------------------------------------
# # ro_0 = DensityMatrix(w_0)

# # if __debug__:
# #     ro_0.write_to_file(filename=config.ro_0_csv)
# # -------------------------------------------------------------------------------------------------

# # run(ro_0, H, dt=config.dt, nt=config.nt, config=config, fidelity_mode=True)
# run_w(w_0, H, dt=config.dt, nt=config.nt, config=config, fidelity_mode=True)
# # run(ro_0, H, dt=config.dt, nt=config.nt, config=config, fidelity_mode=False)

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
#     title += "<b>"
#     title += "n = " + str(config.n)
#     if config.capacity - config.n > 0:
#         title += "<br>" + str(config.capacity - config.n) + \
#             " фотонов в полости"
#     # else:
#     # title += "<br>" + "empty cavity"

#     # title += "<br>atoms state: |Ψ<sub>0</sub> i = |11...1>A<sub>0</sub> |00...0>A<sub>1</sub> |vaki<sub>p</sub>" + \
#     #     str(config.init_state)
#     title += "<br>"
#     title += "<br>w<sub>c</sub> = " + wc_str(config.wc)
#     title += "<br>w<sub>a</sub> = " + wa_str(config.wa)
#     title += "<br> g/hw<sub>c</sub> = " + str(config.g/config.wc)
#     title += "<br>"
#     title += "<br>"
#     title += "</b>"

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
