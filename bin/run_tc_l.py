# -------------------------------------------------------------------------------------------------
# TCL
from PyQuantum.TCL.Cavity import Cavity
from PyQuantum.TCL.Hamiltonian import *

from PyQuantum.TCL.WaveFunction import *
from PyQuantum.TCL.DensityMatrix import *

from PyQuantum.TCL.Evolution import *
# -------------------------------------------------------------------------------------------------
# Common
from PyQuantum.Common.LoadPackage import *
from PyQuantum.Common.STR import *

from PyQuantum.Common.Tools import mkdir
from PyQuantum.Common.Print import *
from PyQuantum.Common.PyPlot import PyPlot3D
from PyQuantum.TC.PlotBuilder3D import PlotBuilder3D

# from shutil import copyfile
# from numpy.random import rand

import math
# -------------------------------------------------------------------------------------------------
import argparse

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--config', type=str)

args = parser.parse_args()

if args.config is None:
    import PyQuantum.TCL.config as config
else:
    config = load_pkg("config", args.config)

mkdir(config.path)
# copyfile("PyQuantum/TC/config.py", config.path + '/config.py')
# -------------------------------------------------------------------------------------------------
cavity = Cavity(wc=config.wc, wa=config.wa, g=config.g,
                n_atoms=config.n_atoms, n_levels=config.n_levels)

cavity.print()
# -------------------------------------------------------------------------------------------------
print("T:", config.T)
print("nt:", config.nt)
print("dt:", config.dt)

print()
# -------------------------------------------------------------------------------------------------
H = Hamiltonian(capacity=config.capacity,
                cavity=cavity, RWA=True, reduced=True)

H.to_html("H.html")
# print(dir(Hamiltonian))
print("H written")
# # H = Hamiltonian(capacity=config.capacity,
# #                 cavity=cavity, RWA=True, reduced=True)

# # for k, v in H.states.items():
# #     print(k, ":", v)
# # exit(0)
# # H.iprint()


# # H.print_html()


# # # H = Hamiltonian(capacity=config.capacity, cavity=cavity)

w_0 = WaveFunction(states=H.states, init_state=config.init_state)
print("w_0")

ro_0 = DensityMatrix(w_0)
print("ro_0")

run(ro_0, H, dt=config.dt, nt=config.nt,
    l=config.l, config=config)

if not __debug__ or __debug__:
    plt = PlotBuilder3D()

    plt.set_width(950)
    plt.set_height(800)
    # ---------------------------------------------- TITLE --------------------------------------------
    title = ""

    if config.capacity - config.n_atoms > 0:
        title += "<b>" + str(config.capacity - config.n) + \
            " фотонов в полости" + "</b>" + "<br><br>"
    else:
        title += "<b>" + "empty cavity" + "</b>" + "<br><br>"

    title += "<b>"
    title += "n_atoms = " + str(config.n_atoms)

    # title += "<br>atoms state: |Ψ<sub>0</sub> i = |11...1>A<sub>0</sub> |00...0>A<sub>1</sub> |vaki<sub>p</sub>" + \
    #     str(config.init_state)
    title += "<br>"
    title += "<br>w<sub>c</sub> = " + wc_str(config.wc)
    title += "<br>w<sub>a</sub> = " + wa_str(config.wa)
    title += "<br><br> g/hw<sub>c</sub> = " + str(config.g/config.wc)
    title += "<br>"
    title += "<br>"
    title += "</b>"

    plt.set_title(title)
    # ---------------------------------------------- TITLE --------------------------------------------

    # ---------------------------------------------- SCALE --------------------------------------------
    y_scale = 1

    y_scale = math.pow(config.T / config.mks, -1.0/2)
    print(y_scale)

    plt.set_yscale(y_scale)

    plt.set_xaxis("states")
    plt.set_yaxis("time, " + T_str_mark(config.T))
    plt.set_zaxis("prob.\t\t\t\t\t\t.")
    # ---------------------------------------------- SCALE --------------------------------------------

    plt.plot(
        x_csv=config.x_csv,
        y_csv=config.y_csv,
        z_csv=config.z_csv,
        filename="tc_l"
    )
