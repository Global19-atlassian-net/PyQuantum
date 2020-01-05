# -------------------------------------------------------------------------------------------------
# system
from time import sleep
from math import sqrt
import csv
# -------------------------------------------------------------------------------------------------
# PyQuantum.TC
from PyQuantum.TC.Unitary import *
# -------------------------------------------------------------------------------------------------
# Common
# from PyQuantum.Common.STR import *
# from PyQuantum.Common.Tools import *
from PyQuantum.Common.Quantum.Operators import operator_a, operator_acrossa, operator_L
# -------------------------------------------------------------------------------------------------
# scientific
import numpy as np
import scipy.linalg as lg
from numpy.linalg import multi_dot
# -------------------------------------------------------------------------------------------------
from time import sleep
from PyQuantum.Tools.Units import *
# import peakutils

# import matplotlib
# import matplotlib.pyplot as plt

# from PyQuantum.Common.Fidelity import *
# -------------------------------------------------------------------------------------------------


def run_out_click(args):
    # ---------------------------------------------------------------------------------------------
    ro_0 = args['ro_0'] if 'ro_0' in args else None
    # print(ro_0.data.diagonal())
    Assert(ro_0 is not None, 'param[\'ro_0\'] is not set')
    # ---------------------------------------------------------------------------------------------
    H = args['H'] if 'H' in args else None

    Assert(H is not None, 'param[\'H\'] is not set')
    # ---------------------------------------------------------------------------------------------
    if 'T_list' in args:
        T_list = args['T_list']
        T_list.clear()

    # if 'sink_list' in args:
    #     sink_list = args['sink_list']
    #     sink_list.clear()
    # ---------------------------------------------------------------------------------------------
    dt = args['dt'] if 'dt' in args else None

    Assert(dt is not None, 'param[\'dt\'] is not set')
    # ---------------------------------------------------------------------------------------------
    # print("run starts ...")
    # ---------------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------------
    # Unitary
    U = Unitary(H, dt)

    # if 'U_csv' in args:
    #     U.to_csv(args['U_csv'])

    U_data = U.data

    U_conj = U.conj()
    # ---------------------------------------------------------------------------------------------
    ro_t = ro_0
    # ---------------------------------------------------------------------------------------------
    states_dim = []

    en = 0

    L_out = operator_L(ro_t, args['lindblad']['out'])

    diag_abs = np.abs(ro_t.data.diagonal(), dtype=np.longdouble)

    start_energy = ro_t.energy(
        H.capacity, H.cavity.n_atoms, H.states_bin, diag_abs)
    start_energy = np.sum(start_energy)

    t = 0

    L_op = L_out

    L_type = 'out'

    cnt = 0

    t_in = 0

    T_click = []

    nt = 0
    p_sink_prev = 0

    while True:
        # if t > 0:
            # print('\t'+time_unit_full(t))
        # -----------------------------------------------------------
        ro_t.data = ((U.data).dot(ro_t.data + dt *
                                  L_op(ro_t).data)).dot(U_conj.data)

        # ro_t.normalize()

        # -----------------------------------------------------------
        # print(L_type)
        nt += 1
        t += dt

        if t >= args['time_limit']:
            print('t >= time_limit')
            break

        diag_abs = np.abs(ro_t.data.diagonal(), dtype=np.longdouble)

        energy = ro_t.energy(H.capacity, H.cavity.n_atoms,
                             H.states_bin, diag_abs)
        if L_type == 'out':
            p_sink = start_energy - np.sum(energy)
            # print(p_sink)
            if nt % args['dt_click'] == 0:
                # if nt % 50 == 0:
                p_coin = np.random.random_sample()

                if p_coin <= p_sink:
                    # print('p_sink: ', "{:.3f}".format(np.round(
                    #     p_sink, 3)), ', p_coin: ', "{:.3f}".format(np.round(p_coin, 3)), ' ', time_unit_full(t), sep='')
                    # print(p_sink, p_coin)
                    # print(nt, time_unit_full(t))
                    # exit(0)
                    return t

        # -----------------------------------------------------------

    return cnt


def run_click(args):
    # ---------------------------------------------------------------------------------------------
    ro_0 = H = None

    T = nt = dt = l = None

    U_csv = x_csv = y_csv = z_csv = None

    thres = None

    T_list = sink_list = None

    sink_limit = None

    in_photons = out_photons = None

    lindblad = args['lindblad']

    if 'in_photons' in args:
        in_photons = args['in_photons']
    if 'out_photons' in args:
        out_photons = args['out_photons']
    # ---------------------------------------------------------------------------------------------
    if 'ro_0' in args:
        ro_0 = args['ro_0']

    Assert(ro_0 is not None, 'param[\'ro_0\'] is not set')
    # ---------------------------------------------------------------------------------------------
    if 'H' in args:
        H = args['H']

    Assert(H is not None, 'param[\'H\'] is not set')
    # ---------------------------------------------------------------------------------------------
    if 'l' in args:
        l = args['l']
    # ---------------------------------------------------------------------------------------------
    if 'T' in args:
        T = args['T']

    if 'dt' in args:
        dt = args['dt']

    if 'nt' in args:
        nt = args['nt']

    if 'sink_limit' in args:
        sink_limit = args['sink_limit']

    if 'precision' in args:
        precision = args['precision']
    else:
        precision = 1e-10
    # ---------------------------------------------------------------------------------------------
    if 'U_csv' in args:
        U_csv = args['U_csv']

    if 'x_csv' in args:
        x_csv = args['x_csv']

    if 'y_csv' in args:
        y_csv = args['y_csv']

    if 'z_csv' in args:
        z_csv = args['z_csv']
    # ---------------------------------------------------------------------------------------------
    if 'thres' in args:
        thres = args['thres']

    if 'T_list' in args:
        T_list = args['T_list']
        T_list.clear()

    if 'sink_list' in args:
        sink_list = args['sink_list']
        sink_list.clear()
    # ---------------------------------------------------------------------------------------------
    Assert(dt is not None, 'param[\'dt\'] is not set')
    # ---------------------------------------------------------------------------------------------
    # print("run starts ...")
    # ---------------------------------------------------------------------------------------------
    # Unitary
    U = Unitary(H, dt)

    # if U_csv is not None:
    #     U.to_csv(args['U_csv'])

    U_data = U.data

    U_conj = U.conj()
    # ---------------------------------------------------------------------------------------------
    ro_t = ro_0
    # ---------------------------------------------------------------------------------------------
    if "z_csv" is not None:
        fz_csv = open("z_csv", "w")

    writer = csv.writer(fz_csv, quoting=csv.QUOTE_NONE, lineterminator="\n")

    states_dim = []

    en = 0

    L_ro = L_out = operator_L(ro_t, args['lindblad']['out'])

    diag_abs = np.abs(ro_t.data.diagonal(), dtype=np.longdouble)

    start_energy = ro_t.energy(
        H.capacity, H.cavity.n_atoms, H.states_bin, diag_abs)
    start_energy = np.sum(start_energy)

    t = 0

    ph_out = False

    T_click = []

    while True:
        # for t in range(0, nt+1):
        # -----------------------------------------------------------
        # print("\t", t)
        # print(t, "/", nt)

        diag_abs = np.abs(ro_t.data.diagonal(), dtype=np.longdouble)
        # print(diag_abs)
        energy = ro_t.energy(H.capacity, H.cavity.n_atoms,
                             H.states_bin, diag_abs)
        # print(np.sum(energy))

        p_sink = 1 - np.sum(energy)

        p_coin = np.random.random_sample()
        print('p_sink: ', p_sink, ', p_coin: ', p_coin, sep='')

        if p_coin <= p_sink:
            T_click.append(t)
            # ph_out = True
            break

        if sink_list is None:
            if np.sum(energy) - start_energy > in_photons:
                return False
        # -----------------------------------------------------------
        if "z_csv" is not None:
            writer.writerow(["{:.5f}".format(x) for x in diag_abs])
        # -----------------------------------------------------------
        # T_list
        if T_list is not None:
            T_list.append(t)
        # -----------------------------------------------------------
        if sink_list is not None:
            zero = diag_abs[0]
            sink = start_energy - np.sum(energy[1:H.capacity+1])

            if len(sink_list) != 0 and (sink_list[-1] - sink) > precision:
                print("err:", sink, "<", sink_list[-1])
                exit(0)

            sink_list.append(sink)

            if sink_limit is not None:
                if abs(sink_limit - sink) < precision:
                    return False
        # -----------------------------------------------------------
        ro_t.data = ((U.data).dot(ro_t.data + dt *
                                  L_ro(ro_t).data)).dot(U_conj.data)

        Assert(abs(1 - ro_t.abs_trace()) <=
               args['precision'], "ro is not normed: " + str(ro_t.abs_trace()))

        # ro_t.normalize()
        # -----------------------------------------------------------
        t += dt

    if ph_out:
        return True
    # ---------------------------------------------------------------------------------------------
    if x_csv is not None:
        write_x_not_ind(H.states, x_csv)
    # write_xbp(H.states, config.x_csv, ind=st)

    if y_csv is not None:
        write_t(T_str_v(T), nt, y_csv)
    # ---------------------------------------------------------------------------------------------
    if z_csv is not None:
        fz_csv.close()
    # ---------------------------------------------------------------------------------------------
    return True


def run(args):
    # ---------------------------------------------------------------------------------------------
    ro_0 = H = None

    T = nt = dt = l = None

    U_csv = x_csv = y_csv = z_csv = None

    thres = None

    T_list = sink_list = None

    sink_limit = None

    in_photons = out_photons = None

    lindblad = args['lindblad']

    if 'in_photons' in args:
        in_photons = args['in_photons']
    if 'out_photons' in args:
        out_photons = args['out_photons']
    # ---------------------------------------------------------------------------------------------
    if 'ro_0' in args:
        ro_0 = args['ro_0']

    Assert(ro_0 is not None, 'param[\'ro_0\'] is not set')
    # ---------------------------------------------------------------------------------------------
    if 'H' in args:
        H = args['H']

    Assert(H is not None, 'param[\'H\'] is not set')
    # ---------------------------------------------------------------------------------------------
    if 'l' in args:
        l = args['l']
    # ---------------------------------------------------------------------------------------------
    if 'T' in args:
        T = args['T']

    if 'dt' in args:
        dt = args['dt']

    if 'nt' in args:
        nt = args['nt']

    if 'sink_limit' in args:
        sink_limit = args['sink_limit']

    if 'precision' in args:
        precision = args['precision']
    else:
        precision = 1e-10
    # ---------------------------------------------------------------------------------------------
    if 'U_csv' in args:
        U_csv = args['U_csv']

    if 'x_csv' in args:
        x_csv = args['x_csv']

    if 'y_csv' in args:
        y_csv = args['y_csv']

    if 'z_csv' in args:
        z_csv = args['z_csv']
    # ---------------------------------------------------------------------------------------------
    if 'thres' in args:
        thres = args['thres']

    if 'T_list' in args:
        T_list = args['T_list']
        T_list.clear()

    if 'sink_list' in args:
        sink_list = args['sink_list']
        sink_list.clear()
    # ---------------------------------------------------------------------------------------------
    Assert(dt is not None, 'param[\'dt\'] is not set')
    # ---------------------------------------------------------------------------------------------
    # print("run starts ...")
    # ---------------------------------------------------------------------------------------------
    # a = operator_a(H, H.capacity, H.cavity.n_atoms)
    # acrossa = operator_acrossa(H, H.capacity, H.cavity.n_atoms)

    # across = a.conj()

    # # a.print(precision=3)
    # # print()
    # # across.print(precision=3)
    # # exit(0)

    # if check:
    #     across_a = Matrix(H.size, H.size, dtype=np.longdouble)
    #     across_a.data = lil_matrix((across.data).dot(a.data), dtype=np.longdouble)
    #     # a_cross_a.print()

    #     # across_a__cross = Matrix(H.size, H.size, dtype=np.double)
    #     across_a__cross = across_a.conj()

    # aa_cross = Matrix(H.size, H.size, dtype=np.double)
    # aa_cross.data = (aa.data.dot(aa.data.transpose()))
    # ---------------------------------------------------------------------------------------------
    # Unitary
    U = Unitary(H, dt)
    # print(type(U.data))

    if U_csv is not None:
        U.to_csv(args['U_csv'])

    U_data = U.data

    U_conj = U.conj()
    # print(type(U_conj))
    # ---------------------------------------------------------------------------------------------
    ro_t = ro_0
    # ---------------------------------------------------------------------------------------------
    if "z_csv" is not None:
        fz_csv = open("z_csv", "w")

    writer = csv.writer(fz_csv, quoting=csv.QUOTE_NONE, lineterminator="\n")

    states_dim = []

    en = 0

    # states_bin = {}

    # for k, v in enumerate(H.states):
    #     en = v[0] + np.sum(v[1])

    #     if en not in states_bin:
    #         states_bin[en] = []

    #     states_bin[en].append(k)

    # if v[0] + np.sum(v[1]) > en:
    #     en += 1
    #     states_dim.append(k-1)

    # print(states_dim)

    # exit(0)
    # ll = across_a.data+across.data
    # ll_cross = ll.getH()

    L_ro = L_out = operator_L(ro_t, args['lindblad']['out'])

    diag_abs = np.abs(ro_t.data.diagonal(), dtype=np.longdouble)

    start_energy = ro_t.energy(
        H.capacity, H.cavity.n_atoms, H.states_bin, diag_abs)
    start_energy = np.sum(start_energy)

    t = 0

    while True:
        # for t in range(0, nt+1):
        # -----------------------------------------------------------
        # print("\t", t)
        # print(t, "/", nt)

        diag_abs = np.abs(ro_t.data.diagonal(), dtype=np.longdouble)
        # print(diag_abs)
        energy = ro_t.energy(H.capacity, H.cavity.n_atoms,
                             H.states_bin, diag_abs)
        print(np.sum(energy))
        if sink_list is None:
            # print(np.round(diag_abs, 3))
            # energy = ro_t.energy(H.capacity, H.cavity.n_atoms, H.states_bin, diag_abs)
            # print("energy:", np.sum(energy))
            # print()
            # sleep(1)

            if np.sum(energy) - start_energy > in_photons:
                # print("init_energy: ", start_energy, ", energy: ", np.sum(
                #     energy[1:]), ", ", np.round(energy, 3), sep="")
                # exit(0)
                return False
        # -----------------------------------------------------------
        # write
        # writer_all.writerow(["{:.5f}".format(x) for x in diag_abs])
        # writer.writerow(["{:.5f}".format(x) for x in v_bin])

        if "z_csv" is not None:
            writer.writerow(["{:.5f}".format(x) for x in diag_abs])
        # -----------------------------------------------------------
        # T_list
        if T_list is not None:
            # sleep(1)
            T_list.append(t)
        # -----------------------------------------------------------
        # print(states_bin)
        # exit(0)
        # sink

        if sink_list is not None:
            # zero = abs(ro_t.data[0, 0])
            zero = diag_abs[0]

            # states_dim = [1, 4, 4, 3]
            # print(np.abs(ro_t.diagonal()))
            # capacity = 1
            # start = states_dim[0]+1

            # energy = [0] * (H.capacity + H.cavity.n_atoms+1)

            # # print(energy)

            # for i in range(1, len(states_bin)):
            #     # print(i)

            #     for j in states_bin[i]:
            #         # print(states_bin[i])
            #         energy[i] += diag_abs[j]
            #     # energy[i] += np.sum(diag_abs[states_bin[i]])
            # energy = ro_t.energy(H.capacity, H.cavity.n_atoms, H.states_bin, diag_abs)
            # for i in range(1, len(states_bin)):
            #     energy[i] *= i
            # for c in states_dim[1:]:
            #     # energy[capacity] = capacity
            #     fin = c+1
            #     # fin = start+c
            #     print(capacity, c, '[', start, ':', fin, ']')
            #     energy[capacity] = np.sum(diag_abs[start:fin]) * (capacity)
            #     # energy[capacity] = np.sum(diag_abs[start:fin]) * (H.capacity-capacity)
            #     print("energy[", capacity, "] = ", np.sum(diag_abs[start:fin]), " * ", (capacity))

            #     # print("cnt =", cnt, energy[cnt], np.sum(energy[cnt]))
            #     capacity += 1
            #     start = fin

            # exit(0)
            # print(np.round(energy, 3))
            # print("energy:", energy)
            # sink = np.sum(energy) - np.sum(energy[1:])
            # sink = np.sum(energy) - np.sum(energy[1:])
            sink = start_energy - np.sum(energy[1:H.capacity+1])
            # st_energy = ((operator_acrossa(H, H.capacity, H.cavity.n_atoms)).data.dot(ro_0.data))
            # st_energy = np.sum(np.abs(start_energy))
            # sink = start_energy - st_energy

            # sink = args['en_'] - np.sum(energy[1:])
            # print("sink:", sink, ", energy:", np.sum(energy[1:H.capacity+1]))
            # sink = H.capacity - np.sum(energy[1:])
            # sink = args['H'].capacity * zero
            # print("sink =", H.capacity, "-", np.sum(energy[1:]))
            # sink = args['H'].capacity * zero
            # print("init_energy: ", start_energy, ", energy: ", np.sum(
            #     energy[1:]), ", ", np.round(energy, 3), ", sink: ", sink, sep="")

            if len(sink_list) != 0 and (sink_list[-1] - sink) > precision:
                print("err:", sink, "<", sink_list[-1])
                exit(0)

            sink_list.append(sink)

            if sink_limit is not None:
                if abs(sink_limit - sink) < precision:
                    return False
        # -----------------------------------------------------------
        # evolution
        # ro_t.data = ro_t.data + dt * L_ro(ro_t).data

        # LL = Matrix(m=ro_t.m, n=ro_t.n, dtype=np.complex128)
        # LL.data = L_ro(ro_t).data
        # print("L_ro:")
        # LL.print()

        # print("ro_t:")
        # ro_t.print()
        # exit(0)

        # ro_t.data = ((U.data).dot(ro_t.data)).dot(U_conj.data)

        ro_t.data = ((U.data).dot(ro_t.data + dt *
                                  L_ro(ro_t).data)).dot(U_conj.data)

        Assert(abs(1 - ro_t.abs_trace()) <=
               args['precision'], "ro is not normed: " + str(ro_t.abs_trace()))

        # ro_t.normalize()
        # -----------------------------------------------------------
        t += dt
        # across_a__cross.print()
        # H.print_states()
        # ro_0.print()
        # sleep(1)

    # ---------------------------------------------------------------------------------------------
    if x_csv is not None:
        write_x_not_ind(H.states, x_csv)
    # write_xbp(H.states, config.x_csv, ind=st)

    if y_csv is not None:
        write_t(T_str_v(T), nt, y_csv)
    # ---------------------------------------------------------------------------------------------
    if z_csv is not None:
        fz_csv.close()
    # ---------------------------------------------------------------------------------------------
    return True

# =====================================================================================================================
# states_dim = [1, 4, 4, 3]
# print(np.abs(ro_t.diagonal()))
# capacity = 1
# start = 1

# print(energy)

# for c in states_dim[1:]:
#     # energy[capacity] = capacity
#     fin = start+c
#     # print(capacity, c, '[', start, ':', fin, ']')
#     energy[capacity] = np.sum(abs_diag[start:fin]) * (3-capacity)
#     # print("cnt =", cnt, energy[cnt], np.sum(energy[cnt]))
#     capacity += 1
#     # cnt += 1
#     start = fin

# exit(0)
# print(np.round(energy, 3))

# print((3-zero) + np.sum(energy))
# print(abs(ro_t.data[0, 0]), args['H'].capacity - np.sum(energy[1:]), energy[1:])
# sleep(3)
# =====================================================================================================================
# diag = ro_t.diagonal()
# diag_abs = np.abs(diag)[0, 0]
# ro_t /= np.linalg.norm(ro_t)
# print(ro_t.toarray())

# print(type(ro_t))
# =====================================================================================================================
# sleep(1)
# peaks = peakutils.indexes(diag_abs, thres=thres)

# for i in peaks:
#     states.add(i)

# print(diag_abs)
# =====================================================================================================================
# st = dict()
# print(diag_abs, np.sum(diag_abs))

# need_states = []

# for k in H.states:
#     if k[0] + np.sum(k[1]) == config.capacity:
#         need_states.append(k)

# for k in range(len(need_states)):
#     if k in states:
#         st[k] = str(need_states[k][1])
#     else:
#         st[k] = ""
# =====================================================================================================================
# L = operator_L(ro_t.data, a, a_cross, across_a)
# ro_t = U_data.dot(ro_t).dot(U_conj_data)
# print(ro_t.count_nonzero(), np.shape(H.matrix.data)[0] * np.shape(H.matrix.data)[1])

# ro_t = U.data.dot(ro_t).dot(U_conj)
# ro_t = sp.csc_matrix(np.array(ro_t))
# ro_t = ro_t + dt * (config.l * L)
# ro_t = ro_t + dt * (config.l * L)
# ro_t = ro_t + dt * (config.l * L)
# print(ro_t.trace()[0, 0])
# =====================================================================================================================
# print(H.states_bin)

# ro_0_sqrt = lg.fractional_matrix_power(
#     ro_0.data[0:5, 0:5], 0.5)

# print(ro_0_sqrt)

# ro_t.print()

# for i in range(H.size):
#     for j in range(H.size):
#         if ro_t.data[i, j] != 0:
#             print(H.states[i], H.states[j])

# print(H.states[j], " -> ", H.states[i], ": ", np.round(a[i][j], 3), sep="")
# =====================================================================================================================
# print(abs(ro_t.data[0, 0]))
# print("ro_t:")
# ro_t.print()

# print()
# sleep(3)


# ro_t = ro_t + dt * -1j * (config.l * L)
# print(type(U_data), type(ro_t), type(U_conj))
# exit(0)
# =====================================================================================================================
# trace_abs = np.sum(diag_abs[0:4])

# print(diag_abs, np.sum(diag_abs))
# print(diag_abs, np.sum(diag_abs))

# Assert(abs(1 - np.sum(diag_abs)) <= 0.1, "ro is not normed")

# writer.writerow(["{:.5f}".format(x) for x in p[k1:k2 + 1]])

# for k, v in p_bin.items():
#     p_bin[k] = 0

# for k, v in H.states_bin.items():
#     for ind in v:
#         p_bin[k] += diag_abs[ind]

# v_bin = [p_bin[k] for k in H.states_bin_keys]

# for i, j in enumerate(v_bin):
#     if abs(j) > thres:
#         states.add(i)
# print(p_bin)
# print(H.states_bin_keys)
# print(H.states)
# print(v_bin)
# =====================================================================================================================
# print(p_bin)
# ro_t = sp.csc_matrix(ro_t)
# U_data = sp.csc_matrix(U.data)
# U_conj_data = sp.csc_matrix(U_conj.data)

# print("bin:")

# H.print_bin_states()
# print(p_bin)
# =====================================================================================================================
# H.states_bin = {}

# for k, v in enumerate(H.states):
#     at_state = str(v[1])

#     if at_state not in H.states_bin:
#         H.states_bin[at_state] = []

#     H.states_bin[at_state].append(k)

# H.states_bin_keys = H.states_bin.keys()

# p_bin = dict.fromkeys(H.states_bin_keys)
# =====================================================================================================================
# sink = 1
# capacity = H.capacity
# cnt = 0
# energy = [0] * (H.capacity+H.cavity.n_atoms)
# sink_list.append(abs_diag[0])

# s = args['H'].capacity * (1 - np.sum(energy[1:]))
# =====================================================================================================================
# def run_in_out(args):
#     # ---------------------------------------------------------------------------------------------
#     ro_0 = H = None

#     T = nt = dt = l = None

#     U_csv = x_csv = y_csv = z_csv = None

#     thres = None

#     T_list = sink_list = None

#     sink_limit = None

#     in_photons = out_photons = None

#     lindblad = args['lindblad']

#     if 'in_photons' in args:
#         in_photons = args['in_photons']
#     if 'out_photons' in args:
#         out_photons = args['out_photons']
#     # ---------------------------------------------------------------------------------------------
#     if 'ro_0' in args:
#         ro_0 = args['ro_0']

#     Assert(ro_0 is not None, 'param[\'ro_0\'] is not set')
#     # ---------------------------------------------------------------------------------------------
#     if 'H' in args:
#         H = args['H']

#     Assert(H is not None, 'param[\'H\'] is not set')
#     # ---------------------------------------------------------------------------------------------
#     if 'l' in args:
#         l = args['l']
#     # ---------------------------------------------------------------------------------------------
#     if 'T' in args:
#         T = args['T']

#     if 'dt' in args:
#         dt = args['dt']

#     if 'nt' in args:
#         nt = args['nt']

#     if 'sink_limit' in args:
#         sink_limit = args['sink_limit']

#     if 'precision' in args:
#         precision = args['precision']
#     else:
#         precision = 1e-10
#     # ---------------------------------------------------------------------------------------------
#     if 'U_csv' in args:
#         U_csv = args['U_csv']

#     if 'x_csv' in args:
#         x_csv = args['x_csv']

#     if 'y_csv' in args:
#         y_csv = args['y_csv']

#     if 'z_csv' in args:
#         z_csv = args['z_csv']
#     # ---------------------------------------------------------------------------------------------
#     if 'thres' in args:
#         thres = args['thres']

#     if 'T_list' in args:
#         T_list = args['T_list']
#         T_list.clear()

#     if 'sink_list' in args:
#         sink_list = args['sink_list']
#         sink_list.clear()
#     # ---------------------------------------------------------------------------------------------
#     Assert(dt is not None, 'param[\'dt\'] is not set')
#     # ---------------------------------------------------------------------------------------------
#     # print("run starts ...")
#     # ---------------------------------------------------------------------------------------------
#     # Unitary
#     U = Unitary(H, dt)
#     # print(type(U.data))

#     if U_csv is not None:
#         U.to_csv(args['U_csv'])

#     U_data = U.data

#     U_conj = U.conj()
#     # print(type(U_conj))
#     # ---------------------------------------------------------------------------------------------
#     ro_t = ro_0
#     # ---------------------------------------------------------------------------------------------
#     if "z_csv" is not None:
#         fz_csv = open("z_csv", "w")

#     writer = csv.writer(fz_csv, quoting=csv.QUOTE_NONE, lineterminator="\n")

#     states_dim = []

#     en = 0

#     L_ro = L_out = operator_L(ro_t, args['lindblad']['out'])

#     diag_abs = np.abs(ro_t.data.diagonal(), dtype=np.longdouble)

#     start_energy = ro_t.energy(
#         H.capacity, H.cavity.n_atoms, H.states_bin, diag_abs)
#     start_energy = np.sum(start_energy)

#     t = 0

#     while True:
#         if t > 0:
#             print('\t'+time_unit_full(t))
#         # for t in range(0, nt+1):
#         # -----------------------------------------------------------
#         # print("\t", t)
#         # print(t, "/", nt)

#         diag_abs = np.abs(ro_t.data.diagonal(), dtype=np.longdouble)
#         print(diag_abs)
#         energy = ro_t.energy(H.capacity, H.cavity.n_atoms,
#                              H.states_bin, diag_abs)

#         if sink_list is None:
#             if np.sum(energy) - start_energy > in_photons:
#                 return False
#         # -----------------------------------------------------------

#         if "z_csv" is not None:
#             writer.writerow(["{:.5f}".format(x) for x in diag_abs])
#         # -----------------------------------------------------------
#         # T_list
#         if T_list is not None:
#             T_list.append(t)
#         # -----------------------------------------------------------

#         if sink_list is not None:
#             zero = diag_abs[0]

#             sink = start_energy - np.sum(energy[1:H.capacity+1])

#             if len(sink_list) != 0 and (sink_list[-1] - sink) > precision:
#                 print("err:", sink, "<", sink_list[-1])
#                 exit(0)

#             sink_list.append(sink)

#             if sink_limit is not None:
#                 if abs(sink_limit - sink) < precision:
#                     return False
#         # -----------------------------------------------------------
#         # evolution

#         ro_t.data = ((U.data).dot(ro_t.data + dt *
#                                   L_ro(ro_t).data)).dot(U_conj.data)

#         Assert(abs(1 - ro_t.abs_trace()) <=
#                args['precision'], "ro is not normed" + str(ro_t.abs_trace()))

#         # -----------------------------------------------------------
#         t += dt

#     # ---------------------------------------------------------------------------------------------
#     if x_csv is not None:
#         write_x_not_ind(H.states, x_csv)

#     if y_csv is not None:
#         write_t(T_str_v(T), nt, y_csv)
#     # ---------------------------------------------------------------------------------------------
#     if z_csv is not None:
#         fz_csv.close()
#     # ---------------------------------------------------------------------------------------------
#     return True
