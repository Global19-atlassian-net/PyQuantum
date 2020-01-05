# -------------------------------------------------------------------------------------------------
# TC
from PyQuantum.TC.Cavity import Cavity
from PyQuantum.TC.Hamiltonian import Hamiltonian

from PyQuantum.TC.WaveFunction import WaveFunction

from PyQuantum.TC.Evolution import run_wf  # ?
# -------------------------------------------------------------------------------------------------
# Common
from PyQuantum.Common.LoadPackage import *
from PyQuantum.Common.STR import *

from PyQuantum.Common.Tools import mkdir
from PyQuantum.Tools.Print import *
from PyQuantum.Tools.PlotBuilder3D import *
# from PyQuantum.TC.PlotBuilder3D import PlotBuilder3D
# from PyQuantum.Common.PyPlot import PyPlot3D

# from shutil import copyfile
# from numpy.random import rand
from PyQuantum.Tools.Hz import *
# -------------------------------------------------------------------------------------------------
import argparse

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--config', type=str)

args = parser.parse_args()

if args.config is None:
    import PyQuantum.TC.config as config
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

cavity.info()
# -------------------------------------------------------------------------------------------------
H = Hamiltonian(
    capacity=config.capacity,
    cavity=cavity,
    RWA=True,
    # reduced=True
)

# H.iprint()

# H.print_html()
# -------------------------------------------------------------------------------------------------
w_0 = WaveFunction(states=H.states, init_state=config.init_state)

w_0.print()
# -------------------------------------------------------------------------------------------------
# run_wf(
#     w_0=w_0,
#     H=H,
#     dt=config.dt,
#     nt=config.nt,
#     config=config,
#     fidelity_mode=False
# )
# -------------------------------------------------------------------------------------------------
title = ""

if config.capacity - config.n_atoms > 0:
    title += "<b>" + str(config.capacity - config.n) + \
        " фотонов в полости" + "</b>" + "<br><br>"
else:
    title += "<b>" + "empty cavity" + "</b>" + "<br><br>"

title += "<b>"
title += "n_atoms = " + str(config.n_atoms)

title += "<br>"

title += "<br>w<sub>c</sub> = " + to_Hz(config.wc)
title += "<br>w<sub>a</sub> = " + to_Hz(config.wa)
title += "<br><br> g/hw<sub>c</sub> = " + str(np.round(config.g/config.wc, 3))

title += "<br>"
title += "<br>"
title += "</b>"

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


plot_builder = PlotBuilder3D({
    'title': title,

    'x_title': 'states',
    'y_title': 'time, ' + T_str_mark(config.T),
    'z_title': 'prob.\t\t\t\t\t\t.',

    'y_scale': y_scale,

    'width': 950,
    'height': 800,

    'x_csv': config.x_csv,
    'y_csv': config.y_csv,
    'z_csv': config.z_csv,

    'x_range': [0, 1],
    'y_range': [0, 1],
    'z_range': [0, 1],

    # 't_coeff': t_coeff,
})

plot_builder.plot(online='False', path='', filename='1.html')
