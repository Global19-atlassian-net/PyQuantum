import PyQuantum.TCH_Full.animator as animator
# -------------------------------------------------------------------------------------------------
# system
import csv
from scipy.linalg import expm
# -------------------------------------------------------------------------------------------------
# BipartiteGeneral
from PyQuantum.TCH_Full.Unitary import *
# -------------------------------------------------------------------------------------------------
# Common
from PyQuantum.Common.ext import *
from PyQuantum.Common.Fidelity import *
# -------------------------------------------------------------------------------------------------
# scientific
import numpy as np
import scipy.linalg as lg
# -------------------------------------------------------------------------------------------------


def get_wdt(wt, exp_iHdt):

    wt = np.dot(exp_iHdt, wt)

    return wt


def get_wt(w0, H, t):
    exp = expm(H * complex(0, -1) * t)

    wt = np.dot(exp, w0)

    return wt


def Run(w0, H, t0, t1, initstate1, initstate2, ph_count1, ph_count2, config, nt=200, not_empty=False, ymin=0, ymax=1, RWA=True, title='title', color='blue'):
    t = np.linspace(t0, t1, nt+1)

    dt = t[1] - t[0]

    # --------------------------------------------------------
    U = Unitary(H, dt)

    if __debug__:
        U.write_to_file(config.U_csv)

    U_conj = U.conj()
    # --------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    state = []

    at1_count = len(initstate1[1])
    at2_count = len(initstate2[1])

    w_0 = np.matrix(w0.data)
    w_t = np.array(w0.data)

    w = []

    with open(config.z_csv, "w") as csv_file:
        writer = csv.writer(
            csv_file, quoting=csv.QUOTE_NONE, lineterminator="\n")

        for t_ in range(0, nt+1):
            w_t_arr = w_t.reshape(1, -1)[0]

            diag_abs = np.abs(w_t_arr)**2
            trace_abs = np.sum(diag_abs)
            w.append(diag_abs)

            Assert(abs(1 - trace_abs) <= 0.1, "ro is not normed", cf())
            # --------------------------------------------------------------------
            writer.writerow(["{:.5f}".format(x)
                             for x in diag_abs])
            # --------------------------------------------------------------------
            w_t = np.array(U.data.dot(w_t))

    w = np.array(w)

    print(w)
    # ------------------------------------------------------------------------------------------------------------------
    # animator.make_plot3D(t, t0, t1, w, ymin=ymin, ymax=ymax, state=state, not_empty=not_empty, max_limit=max_limit)
    st = initstate2[0]*(pow(2, at2_count))

    for i in range(0, at2_count):
        st += pow(2, i) * initstate2[1][at2_count-i-1]

    for i in range(0, at1_count):
        st += (pow(2, i+at2_count) * (ph_count2+1)) * \
            initstate1[1][at1_count-i-1]

    st += initstate1[0] * (pow(2, at1_count + at2_count) * (ph_count2+1))

    print(w[:, st])
    # ------------------------------------------------------------------------------------------------------------------
    # animator.make_plot3D(t, t0, t1, w, ymin=ymin, ymax=ymax, state=state, not_empty=not_empty, max_limit=max_limit)

    animator.make_plot(t, t0, t1, ymin, ymax, w[:, st], color, title=title)

    return


# -------------------------------------------------------------------------------------------------
def run(ro_0, H, dt, nt, config, fidelity_mode=False):
    # --------------------------------------------------------
    U = Unitary(H, dt)

    if __debug__:
        U.write_to_file(config.U_csv)

    U_conj = U.conj()
    # --------------------------------------------------------
    if fidelity_mode:
        ro_0_sqrt = lg.fractional_matrix_power(ro_0.data, 0.5)

        fidelity = []

    ro_t = ro_0.data
    # ----------------------------------------------------------------------------
    p_bin = dict.fromkeys(H.states_bin_keys)
    # --------------------------------------------------------
    with open(config.z_csv, "w") as csv_file:
        writer = csv.writer(
            csv_file, quoting=csv.QUOTE_NONE, lineterminator="\n")

        with open(config.z_all_csv, "w") as csv_all_file:
            writer_all = csv.writer(
                csv_all_file, quoting=csv.QUOTE_NONE, lineterminator="\n")

            for t in range(0, nt):
                diag_abs = np.abs(np.diag(ro_t))

                trace_abs = np.sum(diag_abs)

                Assert(abs(1 - trace_abs) <= 0.1, "ro is not normed", cf())

                for k, v in p_bin.items():
                    p_bin[k] = 0

                for k, v in H.states_bin.items():
                    for ind in v:
                        p_bin[k] += diag_abs[ind]

                v_bin = [p_bin[k] for k in H.states_bin_keys]
                # --------------------------------------------------
                writer.writerow(["{:.5f}".format(x) for x in v_bin])

                # if __debug__:
                # writer_all.writerow(["{:.5f}".format(x) for x in diag_abs])
                # --------------------------------------------------
                if fidelity_mode:
                    fidelity_t = Fidelity(ro_0_sqrt, ro_t)
                    fidelity.append(fidelity_t)
                # --------------------------------------------------
                ro_t = U.data.dot(ro_t).dot(U_conj)
    # --------------------------------------------------------------
    states_bin = {}

    cnt = 0

    for k in H.states_bin_keys:
        if k == "[" + str(0) + "," + str(int(config.n / 2)) + "]" or k == "[" + str(int(config.n / 2)) + "," + str(0) + "]":

            states_bin[cnt] = str(k)
        else:
            states_bin[cnt] = ""
        cnt += 1
    # ----------------------------------------------------------
    states = {}

    cnt = 0

    for v in H.states_bin_keys:
        states[cnt] = v

        cnt += 1
    # ----------------------------------------------------------
    write_x(states, config.x_csv)
    write_t(config.T / config.mks, config.nt, config.y_csv)
    # ----------------------------------------------------------
    if fidelity_mode:
        list_to_csv(fid_csv, fidelity, header=["fidelity"])
    # ----------------------------------------------------------

# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------


def run_wf(w_0, H, dt, nt, config, fidelity_mode=False):
    # --------------------------------------------------------
    U = Unitary(H, dt)

    if __debug__:
        U.write_to_file(config.U_csv)

    U_conj = U.conj()
    # --------------------------------------------------------
    if fidelity_mode:
        fidelity = []

    w_0 = np.matrix(w_0.data)
    w_t = np.array(w_0.data)
    # ----------------------------------------------------------------------------

    atoms = {}
    for k, st in H.states.items():
        arr = []

        for r in range(len(H.cv_chain.cavities)):
            arr.append(st[r][1])

        ind = str(arr)

        if not ind in atoms:
            atoms[ind] = []

        atoms[ind].append(k)

    for k in sorted(atoms.keys()):
        print(k, atoms[k])
    # print(atoms)
    # exit(0)
    p_bin = dict.fromkeys(atoms)
    # --------------------------------------------------------
    # z_0 = []
    # z_1 = []

    # ind_0 = None
    # ind_1 = None

    # i = 0
    # for v in H.states_bin_keys:
    #     print(v)
    #     if v == '[0,'+str(int(H.n/2))+']':
    #         ind_0 = i
    #     elif v == '['+str(int(H.n/2))+',0]':
    #         ind_1 = i

    #     i += 1

    # print(ind_0)
    # print(ind_1)

    with open(config.z_csv, "w") as csv_file:
        writer = csv.writer(
            csv_file, quoting=csv.QUOTE_NONE, lineterminator="\n")

        with open(config.z_all_csv, "w") as csv_all_file:
            writer_all = csv.writer(
                csv_all_file, quoting=csv.QUOTE_NONE, lineterminator="\n")

            dt_ = nt / (config.T/config.mks) / 20000 * 1000
            nt_ = int(nt/dt_)

            for t in range(0, nt):
                w_t_arr = w_t.reshape(1, -1)[0]

                diag_abs = np.abs(w_t_arr)**2
                trace_abs = np.sum(diag_abs)

                Assert(abs(1 - trace_abs) <= 0.1, "ro is not normed", cf())

                for k, v in p_bin.items():
                    p_bin[k] = 0

                for k, v in atoms.items():
                    for ind in v:
                        p_bin[k] += diag_abs[ind]

                v_bin = [p_bin[k] for k in atoms]
                # --------------------------------------------------
                # if t % nt_ == 0:
                writer.writerow(["{:.5f}".format(x) for x in v_bin])

                # z_0.append(round(v_bin[ind_0], 5))
                # z_1.append(round(v_bin[ind_1], 5))
                # print(z_0)
                # print(z_1)
                # exit(1)
                # if __debug__:
                # writer_all.writerow(["{:.5f}".format(x) for x in diag_abs])
                # --------------------------------------------------
                # if fidelity_mode:
                #     w_t = np.matrix(w_t)

                #     D = w_0.getH().dot(w_t).reshape(-1)[0, 0]

                #     fidelity_t = round(abs(D), 3)

                #     fidelity_t = "{:.5f}".format(fidelity_t)

                #     fidelity.append(float(fidelity_t))
                # --------------------------------------------------
                w_t = np.array(U.data.dot(w_t))
    # --------------------------------------------------------------
    # states_bin = {}

    # cnt = 0

    # for k in H.states_bin_keys:
    #     if k == "[" + str(0) + "," + str(int(config.n / 2)) + "]" or k == "[" + str(int(config.n / 2)) + "," + str(0) + "]":

    #         states_bin[cnt] = str(k)
    #     else:
    #         states_bin[cnt] = ""
    #     cnt += 1
    # ----------------------------------------------------------
    # states = {}

    # cnt = 0

    # for v in H.states_bin_keys:
    #     states[cnt] = v

    #     cnt += 1
    # ----------------------------------------------------------
    write_xx(H.states, config.x_csv)
    write_t(T_str_v(config.T), config.nt, config.y_csv)
    # ----------------------------------------------------------
    # if fidelity_mode:
    #     list_to_csv(config.fid_csv, fidelity, header=["fidelity"])

    #     fidelity = fidelity[::nt_]
    #     list_to_csv(config.fid_small_csv, fidelity, header=["fidelity"])

    #     list_to_csv(config.path + 'z_0.csv', z_0, header=["fidelity"])
    #     list_to_csv(config.path + 'z_1.csv', z_1, header=["fidelity"])
    # ----------------------------------------------------------

# -------------------------------------------------------------------------------------------------


# # -------------------------------------------------------------------------------------------------
# # system
# import csv
# # -------------------------------------------------------------------------------------------------
# # Bipartite
# from PyQuantum.TCH.Unitary import *
# # -------------------------------------------------------------------------------------------------
# # Common
# from PyQuantum.Common.ext import *
# from PyQuantum.Common.STR import *
# from PyQuantum.Common.Fidelity import *
# from PyQuantum.Common.Assert import *
# # -------------------------------------------------------------------------------------------------
# # scientific
# import numpy as np
# import scipy.linalg as lg
# # -------------------------------------------------------------------------------------------------

# import PyQuantum.TC.animator as animator


# def get_wdt(wt, exp_iHdt):

#     wt = np.dot(exp_iHdt, wt)

#     return wt


# def run_RWA(w0, H, t0, t1, initstate, certain_state, nt=200, ymin=0, ymax=1, RWA=True, title='title', color='blue'):
#     # ------------------------------------------------------------------------------------------------------------------
#     if not(nt in range(0, 501)):
#         return -1

#     Assert(t0 >= 0, "t0 < 0", cf())
#     Assert(t1 > 0, "t1 <= 0", cf())
#     Assert(t0 < t1, "t0 >= t1", cf())

#     if len(np.shape(H.matrix.data)) != 2:
#         return -1
#     # if np.shape(H)[0] != np.shape(H)[1]:
#         # return -1
#     # if np.shape(H)[0] != len(w0):
#         # return -1
#     # ------------------------------------------------------------------------------------------------------------------
#     nt = t1 * 100

#     t = np.linspace(t0, t1, nt+1)

#     dt = t[1] - t[0]

#     U = Unitary(H, dt)

#     # ------------------------------------------------------------------------------------------------------------------
#     state = []

#     at_count = len(initstate[1])

#     for i in range(0, len(w0.data)):
#         ph_count = int(i / pow(2, at_count))
#         st_number = i % pow(2, at_count)

#         at_binary = bin(st_number)[2:].zfill(at_count)

#         state.append('[' + str(ph_count) + '|' + at_binary + ']')
#     # ------------------------------------------------------------------------------------------------------------------
#     w = []

#     wt = w0

#     for i in range(0, nt+1):
#         wt = get_wdt(wt.data, U.data)

#         Assert(np.max(wt) <= 1, "np.max(wt) > 1", cf())

#         w.append(np.abs(wt))

#     w = np.array(w)
#     w = w[:, :, 0]
#     # ------------------------------------------------------------------------------------------------------------------
#     st = certain_state[0]*(pow(2, at_count))
#     at = 0

#     for i in range(0, at_count):
#         at += pow(2, i) * certain_state[1][at_count-i-1]
#     # ------------------------------------------------------------------------------------------------------------------

#     animator.make_plot(t, t0, t1, ymin, ymax,
#                        w[:, st+at], color, title=title, X=r'$t,\ мкс$', Y=r'$Probability$   ')

#     return


# def run_w(w_0, H, dt, nt, config, fidelity_mode=False):
#     # --------------------------------------------------------
#     U = Unitary(H, dt)

#     if __debug__:
#         U.write_to_file(config.U_csv)

#     U_conj = U.conj()
#     # --------------------------------------------------------
#     if fidelity_mode:
#         fidelity = []

#     w_0 = np.matrix(w_0.data)

#     w_t = np.array(w_0.data)
#     # ----------------------------------------------------------------------------
#     dt_ = nt / (config.T/config.mks) / 20000 * 1000
#     nt_ = int(nt/dt_)

#     z_0 = []
#     z_1 = []
#     z_max = []

#     # ind_0 = None
#     # ind_1 = None

#     # for k, v in H.states.items():
#     #     if v == [0, H.n]:
#     #         ind_0 = k
#     #     elif v == [H.n, 0]:
#     #         ind_1 = k

#     with open(config.z_csv, "w") as csv_file:
#         writer = csv.writer(
#             csv_file, quoting=csv.QUOTE_NONE, lineterminator="\n")

#         for t in range(0, nt+1):
#             w_t_arr = w_t.reshape(1, -1)[0]

#             diag_abs = np.abs(w_t_arr)**2
#             trace_abs = np.sum(diag_abs)

#             Assert(abs(1 - trace_abs) <= 0.1, "ro is not normed", cf())
#             # --------------------------------------------------------------------
#             if fidelity_mode:
#                 w_t = np.matrix(w_t)

#                 D = w_0.getH().dot(w_t).reshape(-1)[0, 0]

#                 fidelity_t = round(abs(D), 3)

#                 fidelity_t = "{:>.5f}".format(fidelity_t)

#                 fidelity.append(fidelity_t)

#             # z_0.append("{:.5f}".format(diag_abs[ind_0]))
#             # z_1.append("{:.5f}".format(diag_abs[ind_1]))

#             # zmax = 0

#             # for i_ in range(0, len(diag_abs)):
#             #     if i_ != ind_0 and i_ != ind_1 and diag_abs[i_] > zmax:
#             #         # exit(1)
#             #         zmax = diag_abs[i_]

#             # z_max.append(zmax)

#             # z_1.append(round(diag_abs[ind_1], config.precision))
#             # z_1.append(float(diag_abs[ind_1]))

#             # if t % nt_ == 0:
#             writer.writerow(["{:.5f}".format(x)
#                              for x in diag_abs])
#             # --------------------------------------------------------------------
#             w_t = np.array(U.data.dot(w_t))
#     # ----------------------------------------------------------------------------
#     states = H.states

#     write_x(states, config.x_csv, ind=[[1, [1, 1, 0]], [1, [0, 1, 1]], [1, [1, 0, 1]], [2, [0, 1, 0]], [
#             2, [0, 0, 1]], [2, [1, 0, 0]], [3, [0, 0, 0]]])
#     # write_x(states, config.x_csv, ind=[[0, H.n], [H.n, 0]])
#     write_t(T_str_v(config.T), config.nt, config.y_csv)
#     # -------------------------v

#     # list_to_csv(config.path + 'z_max.csv', z_max, header=["fidelity"])
#     # list_to_csv(config.path + 'z_0.csv', z_0, header=["fidelity"])
#     # list_to_csv(config.path + 'z_1.csv', z_1, header=["fidelity"])
#     # ----------------------------------------------------------

# # -------------------------------------------------------------------------------------------------
