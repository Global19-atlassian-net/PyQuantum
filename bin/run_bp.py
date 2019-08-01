# -------------------------------------------------------------------------------------------------
# Bipartite
from PyQuantum.Bipartite.Cavity import Cavity

from PyQuantum.Bipartite.Hamiltonian import Hamiltonian

from PyQuantum.Bipartite.WaveFunction import WaveFunction

from PyQuantum.Bipartite.Evolution import run_wf
# -------------------------------------------------------------------------------------------------
# Common
from PyQuantum.Common.STR import *
from PyQuantum.Common.LoadPackage import *

from PyQuantum.Common.Tools import mkdir
from PyQuantum.Tools import Hz
from PyQuantum.Common.PlotBuilder3D import *

from shutil import copyfile
# -------------------------------------------------------------------------------------------------
config = load_pkg("config", "PyQuantum/Bipartite/config.py")

mkdir(config.path)

copyfile("PyQuantum/Bipartite/config.py", config.path + '/config.py')
# -------------------------------------------------------------------------------------------------
# Cavity
cavity = Cavity(n=config.n, wc=config.wc, wa=config.wa, g=config.g)

cavity.print()
# -------------------------------------------------------------------------------------------------
# Hamiltonian
H = Hamiltonian(capacity=config.capacity, cavity=cavity)

print(len(H.states))
H.print_states()
# H.to_csv("H.csv")

# df = pd.DataFrame(H.matrix.data)

# print(df)
# df.to_csv("H.csv2", float_format='%.3f')
if __debug__:
    H.to_csv(filename=config.H_csv)

    H.to_csv("H.csv")
    # H.print_html(filename=config.H_html)
# -------------------------------------------------------------------------------------------------
# WaveFunction
w_0 = WaveFunction(states=H.states, init_state=config.init_state)

if __debug__:
    w_0.print()
# -------------------------------------------------------------------------------------------------
# DensityMatrix
# ro_0 = DensityMatrix(w_0)

# if __debug__:
    # ro_0.to_csv(filename=config.ro_0_csv)
# -------------------------------------------------------------------------------------------------

# run(ro_0=ro_0, H=H, dt=config.dt, nt=config.nt, config=config)
run_wf(w_0=w_0, H=H, dt=config.dt, nt=config.nt,
       config=config, fidelity_mode=True)

# -------------------------------------------------------------------------------------------------

y_scale = 1

if config.T < 0.5 * config.mks:
    y_scale = 0.1
elif config.T == 0.5 * config.mks:
    y_scale = 0.01
elif config.T == 1 * config.mks:
    y_scale = 7.5
    # y_scale = 10
elif config.T == 5 * config.mks:
    y_scale = 1


plt = PlotBuilder3D()


if not __debug__ or __debug__:
    # title = ""
    title = "<b>"
    title += "n = " + str(config.n)
    if config.capacity - config.n > 0:
        title += "<br>" + str(config.capacity - config.n) + \
            " photons in cavity"
    title += "<br>atoms state: " + str(config.init_state)
    title += "<br>"
    title += "<br>w<sub>c</sub> = " + Hz(config.wc)
    title += "<br>w<sub>a</sub> = " + Hz(config.wa)
    title += "<br>g</sub> = " + Hz(config.g)
    title += "</b>"

    plt.set_title(title)

    plt.set_xaxis("states")
    plt.set_yaxis("time, " + T_str_mark(config.T))
    plt.set_zaxis("prob.")

    plt.set_yscale(y_scale)

    plt.set_width(1200)
    plt.set_height(650)

    plt.PyPlot3D(
        z_csv=config.path + "/" + "z.csv",
        x_csv=config.path + "/" + "x.csv",
        y_csv=config.path + "/" + "t.csv",
        # t_coeff=20000 / 1000 * (config.T / 1e-6),
        online=False,
        path=config.path,
        filename="Bipartite",
    )
# -------------------------------------------------------------------------------------------------

# fid_plot = True
# # fid_plot = False

# if fid_plot:
#     from PyQuantum.py import *

#     def plot_fidelity(filename=config.fid_csv):
#         z_data = pd.read_csv(filename)

#         t = np.around(np.linspace(0, config.nt, config.nt), 3)

#         title = ""
#         title += "<span style='font-size:18'>"
#         title += "<b>Fidelity</b>"
#         title += "</span>"
#         # title += "<br>"
#         # title += "<span style='font-size:11'>"
#         # title += "n = " + str(config.n)
#         # title += "<br>init. state: " + str(config.init_state)
#         # # title += "<br>t = " + T_str(config.T)
#         # title += "<br>"
#         # title += "<br>w<sub>c</sub> = " + Hz(config.wc)
#         # title += "<br>w<sub>a</sub> = " + wa_str(config.wa)
#         # title += "<br>g = " + g_str(config.g)
#         # title += "</span>"

#         PYPLOT2D(
#             data_0={
#                 "title": title,
#                 # "title": "<b>w<sub>c</sub> = w<sub>a</sub> = 2 PI x 0.5 MHz;\tg / (hw<sub>c</sub>) = 0.001<br>" +
#                 # "m = g<b>",
#                 "x": {
#                     "title": "Time, " + T_str_mark(config.T),
#                     "data": t,

#                     "ticktext": np.around(np.linspace(0, T_str_v(config.T), 11), 3),
#                     "tickvals": np.around(np.linspace(0, config.nt, 11), 3)
#                 },
#                 "y":
#                 {
#                     "title": "Fidelity",
#                     "data": [
#                         z_data["fidelity"],
#                     ]
#                 },
#             },
#             online=False,
#             filename=config.path + "/" + "Fidelity"
#         )

#         return
#         # --------------------------------

#     def plot_fidelity_small(filename=config.fid_csv):
#         z_data = pd.read_csv(filename)

#         t = np.around(np.linspace(0, config.nt, config.nt), 3)

#         title = ""
#         title += "<span style='font-size:18'>"
#         title += "<b>Fidelity</b>"
#         title += "</span>"
#         # title += "<br>"
#         # title += "<span style='font-size:11'>"
#         # title += "n = " + str(config.n)
#         # title += "<br>init. state: " + str(config.init_state)
#         # # title += "<br>t = " + T_str(config.T)
#         # title += "<br>"
#         # title += "<br>w<sub>c</sub> = " + Hz(config.wc)
#         # title += "<br>w<sub>a</sub> = " + wa_str(config.wa)
#         # title += "<br>g = " + g_str(config.g)
#         # title += "</span>"

#         PYPLOT2D(
#             data_0={
#                 "title": title,
#                 # "title": "<b>w<sub>c</sub> = w<sub>a</sub> = 2 PI x 0.5 MHz;\tg / (hw<sub>c</sub>) = 0.001<br>" +
#                 # "m = g<b>",
#                 "x": {
#                     "title": "Time, " + T_str_mark(config.T),
#                     "data": t,

#                     "ticktext": np.around(np.linspace(0, T_str_v(config.T), 11), 3),
#                     "tickvals": np.around(np.linspace(0, config.nt, 11), 3)
#                 },
#                 "y":
#                 {
#                     "title": "Fidelity",
#                     "data": [
#                         z_data["fidelity"],
#                     ]
#                 },
#             },
#             online=False,
#             filename=config.path + "/" + "Fidelity_small"
#         )

#         return
#         # --------------------------------
#     plot_fidelity(config.fid_csv)
    # plot_fidelity(config.fid_small_csv)
    # plot_fidelity_small(config.fid_small_csv)

# if not __debug__:
#     title = "<b>"
#     title += "capacity = " + str(config.capacity) + ", n = " + str(config.n)

#     title += "<br>w<sub>c</sub> = " + Hz(config.wc)
#     title += "<br>w<sub>a</sub> = " + \
#         "[" + ", ".join([wa_str(i) for i in config.wa]) + "]"
#     title += "<br>g = " + "[" + ", ".join([g_str(i) for i in config.g]) + "]"
#     title += "<br>t = " + T_str(config.T)
#     title += "</b>"

#     PyPlot3D(
#         title=title,
#         z_csv=config.path + "/" + "z.csv",
#         x_csv=config.path + "/" + "x.csv",
#         y_csv=config.path + "/" + "t.csv",
#         online=False,
#         path=config.path,
#         filename="Bipartite",
#         xaxis="states",
#         yaxis="time, mks",
#         y_scale=y_scale
#     )
# # -------------------------------------------------------------------------------------------------

# # -------------------------------------------------------------------------------------------------
# # from py import *


# # def plot_fidelity(filename=fid_csv):
# #     z_data = pd.read_csv(filename)

# #     t = np.around(np.linspace(0, nt, nt), 3)

# #     PYPLOT2D(
# #         data_0={
# #             "title": "<b>Fidelity</b>",
# #             # "title": "<b>w<sub>c</sub> = w<sub>a</sub> = 2 PI x 0.5 MHz;\tg / (hw<sub>c</sub>) = 0.001<br>" +
# #             # "m = g<b>",
# #             "x": {
# #                 "title": "Time, mks",
# #                 "data": t,

# #                 "ticktext": np.around(np.linspace(0, T * 1e6, 11), 3),
# #                 "tickvals": np.around(np.linspace(0, config.nt, 11), 3)
# #             },
# #             "y":
# #             {
# #                 "title": "Fidelity",
# #                 "data": [
# #                     z_data["fidelity"],
# #                 ]
# #             },
# #         },
# #         online=False,
# #         filename=path + "/" + "Fidelity"#     )

# #     return
# # -------------------------------------------------------------------------------------------------

# # plot_fidelity()


# # # print([0, [0] * 3 + [1] * 3])
# # st1 = [0, [0, 0, 0, 1, 1, 1]]
# # st2 = [0, [1, 1, 1, 0, 0, 0]]

# # w_0.set_ampl(state=init_state, ampl=0)
# # A = rand(2, 2)
# # A_comp = A.view(dtype=np.complex128)

# # # w_0.set_ampl(state=st1, ampl=1)
# # # w_0.set_ampl(state=st2, ampl=1)

# # w_0.set_ampl(state=st1, ampl=A_comp[0][0])
# # w_0.set_ampl(state=st2, ampl=A_comp[1][0])

# # B = rand(len(H.states), 2)
# # B_comp = B.view(dtype=np.complex128)
# # print(B_comp)
# # for k, v in H.states.items():
# #     w_0.set_ampl(state=v, ampl=B_comp[k][0])

# # w_0.normalize()
# # w_0.print()

# # # exit(1)
