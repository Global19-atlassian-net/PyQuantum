# -------------------------------------------------------------------------------------------------
# TC
from PyQuantum.TC.PlotBuilder3D import PlotBuilder3D
from PyQuantum.TC.Cavity import Cavity
from PyQuantum.TC.Hamiltonian import Hamiltonian

from PyQuantum.TC.WaveFunction import WaveFunction
from PyQuantum.TC.DensityMatrix import DensityMatrix

from PyQuantum.TC.Evolution import run_ro  # ?
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
import argparse

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--config', type=str)

args = parser.parse_args()

if args.config is None:
    config = load_pkg("config", "PyQuantum/TC/config.py")
else:
    config = load_pkg("config", args.config)

mkdir(config.path)
# copyfile("PyQuantum/TC/config.py", config.path + '/config.py')
# -------------------------------------------------------------------------------------------------
cavity = Cavity(
    wc=config.wc,
    wa=config.wa,
    g=config.g,
    n_atoms=config.n_atoms,
    n_levels=config.n_levels
)

cavity.print()
# -------------------------------------------------------------------------------------------------
H = Hamiltonian(
    capacity=config.capacity,
    cavity=cavity,
    RWA=True,
    reduced=True
)

# H.iprint()

# H.print_html()
# -------------------------------------------------------------------------------------------------
w_0 = WaveFunction(states=H.states, init_state=config.init_state)
w_0.print()
# -------------------------------------------------------------------------------------------------
ro_0 = DensityMatrix(w_0)

run_ro(ro_0, H, dt=config.dt, nt=config.nt, config=config, fidelity_mode=True)
# -------------------------------------------------------------------------------------------------
plt = PlotBuilder3D()

plt.set_width(950)
plt.set_height(800)

title = ""

if config.capacity - config.n_atoms > 0:
    title += "<b>" + str(config.capacity - config.n) + \
        " фотонов в полости" + "</b>" + "<br><br>"
else:
    title += "<b>" + "empty cavity" + "</b>" + "<br><br>"

title += "<b>"
title += "n_atoms = " + str(config.n_atoms)

title += "<br>"
title += "<br>w<sub>c</sub> = " + wc_str(config.wc)
title += "<br>w<sub>a</sub> = " + wa_str(config.wa)
title += "<br><br> g/hw<sub>c</sub> = " + str(config.g/config.wc)
title += "<br>"
title += "<br>"
title += "</b>"

plt.set_title(title)

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

plt.set_yscale(y_scale)

plt.set_xaxis("states")
plt.set_yaxis("time, " + T_str_mark(config.T))
plt.set_zaxis("prob.\t\t\t\t\t\t.")

plt.plot(
    x_csv=config.x_csv,
    y_csv=config.y_csv,
    z_csv=config.z_csv,
)
