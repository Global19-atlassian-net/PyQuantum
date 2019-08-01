# ---------------------------------------------------------------------------------------------------------------------
# TC_Lindblad
# import matplotlib
# import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib
from PyQuantum.Common.STR import *
import numpy as np
from PyQuantum.PlotBuilder.PlotBuilder3D import PlotBuilder3D
from PyQuantum.Common.PyPlot import PyPlot3D
# from PyQuantum.Common.STR import *
import PyQuantum.TC_Lindblad.config as config
from PyQuantum.TC_Lindblad.Cavity import Cavity
# from PyQuantum.TC_Lindblad.Hamiltonian import Hamiltonian
from PyQuantum.TC_Lindblad.Hamiltonian import Hml

from PyQuantum.TC_Lindblad.WaveFunction import WaveFunction
from PyQuantum.TC_Lindblad.DensityMatrix import DensityMatrix

from PyQuantum.TC_Lindblad.Evolution import run
# ---------------------------------------------------------------------------------------------------------------------
from PyQuantum.Common.Tools import mkdir
mkdir(config.path)
# ---------------------------------------------------------------------------------------------------------------------
cavity = Cavity(config.wc, config.wa, config.g, config.n_atoms)
# x = [1, 2]
# y = [1, 2]
# plt.plot(x, y)
# plt.show()
# exit(0)

cavity.info()
# ---------------------------------------------------------------------------------------------------------------------
# H = Hamiltonian(config.capacity, cavity)
H = Hml(config.capacity, cavity)


# H.print()
# print(len(H.states), np.shape(H.matrix.data), type(H.matrix.data),
#       H.matrix.data.getnnz(), '/', np.shape(H.matrix.data)[0]*np.shape(H.matrix.data)[1])
# exit(0)
# ---------------------------------------------------------------------------------------------------------------------
# print(config.init_state)

w_0 = WaveFunction(states=H.states, init_state=config.init_state)
# ---------------------------------------------------------------------------------------------------------------------
ro_0 = DensityMatrix(w_0)

# ro_0.print()
# ---------------------------------------------------------------------------------------------------------------------
sink_list = []
T_list = []

run({
    "ro_0": ro_0,
    "H": H,
    "T": config.T,
    "dt": config.dt,
    "nt": config.nt,
    "l": config.l,
    "thres": 0.1,
    "x_csv": config.x_csv,
    "y_csv": config.y_csv,
    "z_csv": config.z_csv,
    "sink_list": sink_list,
    "T_list": T_list,
})

plt.plot(T_list, sink_list)

for i in sink_list:
    print(i)

plt.show()

# ---------------------------------------------------------------------------------------------------------------------
exit(0)

y_scale = 1

if config.T <= 0.5 * config.mks:
    y_scale = 0.05
elif config.T == 0.5 * config.mks:
    y_scale = 0.01
elif config.T == 1 * config.mks:
    y_scale = 7.5
    # y_scale = 10
elif config.T == 5 * config.mks:
    y_scale = 1

plt = PlotBuilder3D()

title = "<b>"
# title += "capacity = " + str(config.capacity) + ", n = " + str(config.n_atoms)
# title += "<br>w<sub>c</sub> = " + wc_str(config.wc)
# title += "<br>w<sub>a</sub> = " + \
#     "[" + ", ".join([wa_str(i) for i in config.wa]) + "]"
# title += "<br>g = " + "[" + ", ".join([g_str(i) for i in config.g]) + "]"
# title += "<br>t = " + T_str(config.T)
# title += "<br>l = " + wc_str(config.l)
title += "</b>"

plt.set_title(title)

plt.set_xaxis("states")
plt.set_yaxis("time, " + T_str_mark(config.T))
plt.set_zaxis("prob.")

plt.set_yscale(y_scale)

plt.set_width(900)
plt.set_height(650)

plt.plot(
    x_csv=config.x_csv,
    y_csv=config.path + "/" + "t.csv",
    z_csv=config.path + "/" + "z.csv",
    # t_coeff=20000 / 1000 * (config.T / 1e-6),
    online=False,
    path=config.path,
    filename="BipartiteGeneralLindblad",
)
# ---------------------------------------------------------------------------------------------------------------------
