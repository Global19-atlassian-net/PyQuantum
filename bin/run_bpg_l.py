# -------------------------------------------------------------------------------------------------
# system
from PyQuantum.Common.STR import *
import sys
# -------------------------------------------------------------------------------------------------
# BipartiteGeneralLindblad
from PyQuantum.BipartiteGeneralLindblad.Cavity import *
from PyQuantum.BipartiteGeneralLindblad.Hamiltonian import *

from PyQuantum.BipartiteGeneralLindblad.WaveFunction import *
from PyQuantum.BipartiteGeneralLindblad.DensityMatrix import *

from PyQuantum.BipartiteGeneralLindblad.Evolution import *
# -------------------------------------------------------------------------------------------------
# Common
from PyQuantum.Common.LoadPackage import *

from PyQuantum.Common.Tools import mkdir
from PyQuantum.Common.PyPlot import PyPlot3D
# -------------------------------------------------------------------------------------------------
config = load_pkg("config", "PyQuantum/BipartiteGeneralLindblad/config.py")
# -------------------------------------------------------------------------------------------------
mkdir(config.path)
# -------------------------------------------------------------------------------------------------
# print(config.wc)
cavity = Cavity(n=config.n, wc=config.wc, wa=config.wa, g=config.g)

cavity.print_n()
cavity.print_wc()
cavity.print_wa()
cavity.print_g()
# -------------------------------------------------------------------------------------------------
H = Hamiltonian(capacity=config.capacity, cavity=cavity)
# H.print_states()
# print(len(H.states))
# exit(0)
if __debug__:
    H.to_csv(filename=config.H_csv)

    # H.print_bin_states()
    # H.print_html(filename=H_html)
# -------------------------------------------------------------------------------------------------
w_0 = WaveFunction(states=H.states, init_state=config.init_state)

# if __debug__:
# w_0.print()
# -------------------------------------------------------------------------------------------------
ro_0 = DensityMatrix(w_0)

# if __debug__:
# ro_0.to_csv(filename=ro_0_csv)
# -------------------------------------------------------------------------------------------------

run(ro_0=ro_0, H=H, dt=config.dt, nt=config.nt, l=config.l, config=config)

# -------------------------------------------------------------------------------------------------

y_scale = 1

if config.T == 0.05 * config.mks:
    y_scale = 0.1
elif config.T == 0.5 * config.mks:
    y_scale = 0.01
elif config.T == 1 * config.mks:
    y_scale = 7.5
    # y_scale = 10
elif config.T == 5 * config.mks:
    y_scale = 1

plt = PlotBuilder3D()

title = "<b>"
title += "capacity = " + str(config.capacity) + ", n = " + str(config.n)
title += "<br>w<sub>c</sub> = " + wc_str(config.wc)
title += "<br>w<sub>a</sub> = " + \
    "[" + ", ".join([wa_str(i) for i in config.wa]) + "]"
title += "<br>g = " + "[" + ", ".join([g_str(i) for i in config.g]) + "]"
title += "<br>t = " + T_str(config.T)
title += "<br>l = " + wc_str(config.l)
title += "</b>"

plt.set_title(title)

plt.set_xaxis("states")
plt.set_yaxis("time, " + T_str_mark(config.T))
plt.set_zaxis("prob.")

plt.set_yscale(y_scale)

plt.set_width(900)
plt.set_height(650)

plt.plot(
    x_csv=config.path + "/" + "x.csv",
    y_csv=config.path + "/" + "t.csv",
    z_csv=config.path + "/" + "z.csv",
    # t_coeff=20000 / 1000 * (config.T / 1e-6),
    online=False,
    path=config.path,
    filename="BipartiteGeneralLindblad",
)
# -------------------------------------------------------------------------------------------------
