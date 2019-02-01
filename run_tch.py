# system
import itertools
import sys

# TCH
from PyQuantum.TCH.Cavity import Cavity
from PyQuantum.TCH.CavityChain import CavityChain
from PyQuantum.TCH.Hamiltonian import Hamiltonian

from PyQuantum.TCH.WaveFunction import WaveFunction
from PyQuantum.TCH.DensityMatrix import *
from PyQuantum.TCH.FullBase import *

from PyQuantum.TCH.Evolution import *

# Common
from PyQuantum.Common.LoadPackage import *
from PyQuantum.Common.STR import *

from PyQuantum.Common.ext import mkdir
from PyQuantum.Common.Print import *
from PyQuantum.Common.PyPlot import PyPlot3D
# from shutil import copyfile
# from numpy.random import rand

import PyQuantum.TCH.config as config
# config = load_pkg("config", "PyQuantum/TC/config.py")

mkdir(config.path)
# copyfile("PyQuantum/TC/config.py", config.path + '/config.py')

cavity_1 = Cavity(n=config.n_1, wc=config.wc_1, wa=config.wa_1, g=config.g_1)

cavity_1.print(title="Cavity 1:")

cavity_2 = Cavity(n=config.n_2, wc=config.wc_2, wa=config.wa_2, g=config.g_2)

cavity_2.print(title="Cavity 2:")

cv_chain = CavityChain([cavity_1, cavity_2])

print("T:", config.T)
print("nt:", config.nt)
print("dt:", config.dt)

print()

H = Hamiltonian(capacity=config.capacity,
                cv_chain=cv_chain, RWA=True, mu=config.mu)
H.write_to_file(filename=config.H_csv)
H.iprint_symb()

print(16)
exit(0)

H.print_states()

H.print()
w_0 = WaveFunction(states=H.states, init_state=config.init_state)

w_0.print()

run_wf(w_0=w_0, H=H, dt=config.dt, nt=config.nt,
       config=config, fidelity_mode=True)

# -------------------------------------------------------------------------------------------------
title = r'$RWA$'+'\n'
color = 'blue'
# run_RWA(w0=w_0, H=H, t0=0, t1=config.T, nt=config.nt, initstate=config.init_state,
#         certain_state=config.init_state, ymin=0, ymax=1.005, title=title, color=color)

# exit(0)

# -------------------------------------------------------------------------------------------------
# H_field = H.get_Hfield()
# H_atoms = H.get_Hatoms()
# H_int_RWA = H.get_Hint_RWA()


y_scale = 1

if config.T < 0.25 * config.mks:
    y_scale = 0.1
elif config.T <= 0.5 * config.mks:
    y_scale = 0.025
elif config.T == 0.5 * config.mks:
    y_scale = 0.01
elif config.T == 1 * config.mks:
    y_scale = 7.5
    # y_scale = 10
elif config.T == 5 * config.mks:
    y_scale = 1


if not __debug__ or __debug__:
    title = ""
    # title += "<b>"
    # title += "n = " + str(config.n)
    # if config.capacity - config.n > 0:
    #     title += "<br>" + str(config.capacity - config.n) + \
    #         " фотонов в полости"
    # # else:
    # # title += "<br>" + "empty cavity"

    # # title += "<br>atoms state: |Ψ<sub>0</sub> i = |11...1>A<sub>0</sub> |00...0>A<sub>1</sub> |vaki<sub>p</sub>" + \
    # #     str(config.init_state)
    # title += "<br>"
    # title += "<br>w<sub>c</sub> = " + wc_str(config.wc)
    # title += "<br>w<sub>a</sub> = " + wa_str(config.wa)
    # title += "<br> g/hw<sub>c</sub> = " + str(config.g/config.wc)
    # title += "<br>"
    # title += "<br>"
    # title += "</b>"

    PyPlot3D(
        title=title,
        z_csv=config.path + "/" + "z.csv",
        x_csv=config.path + "/" + "x.csv",
        y_csv=config.path + "/" + "t.csv",
        # t_coeff=20000 / 1000 * (config.T / 1e-6),
        online=False,
        path=config.path,
        filename="Bipartite",
        xaxis="states",
        yaxis="time, " + T_str_mark(config.T),
        y_scale=y_scale
    )
