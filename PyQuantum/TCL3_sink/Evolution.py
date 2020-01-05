# ---------------------------------------------------------------------------------------------------------------------
# system
from time import sleep
from math import sqrt
import csv
# ---------------------------------------------------------------------------------------------------------------------
# scientific
import numpy as np
import scipy.linalg as lg
from numpy.linalg import multi_dot
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.TC
from PyQuantum.TC_sink.Unitary import *
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Tools
from PyQuantum.Tools.Units import *
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Common
from PyQuantum.Common.Quantum.Operators import operator_a, operator_a3, operator_acrossa, operator_L
# ---------------------------------------------------------------------------------------------------------------------



# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------- RUN_OUT_CLICK ----------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
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

    L_RO = []
    L_OUT = []

    for i in args['lindblad']['out']:
        L_ = operator_L(ro_t, i)
        L_RO.append(L_)
        L_OUT.append(L_)
    start_energy = ro_t.energy(
        H.capacity, H.cavity.n_atoms, H.states_bin, diag_abs)

    start_energy['0_1'] = np.sum(start_energy['0_1'])
    start_energy['1_2'] = np.sum(start_energy['1_2'])

    sink = {}

    # start_energy = ro_t.energy(
    #     H.capacity, H.cavity.n_atoms, H.states_bin, diag_abs)
    # start_energy = np.sum(start_energy)

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
            # p_sink = start_energy - np.sum(energy)
            sink['0_1'] = start_energy['0_1'] - \
                np.sum(energy['0_1'])
            sink['1_2'] = start_energy['1_2'] - \
                np.sum(energy['1_2'])
                
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


# ---------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------- RUN --------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
def run(args):
    ro_0 = H = None

    T = nt = dt = l = None

    U_csv = x_csv = y_csv = z_csv = None

    thres = None

    T_list = sink_list = None

    sink_limit = None

    in_photons = out_photons = None

    lindblad = args['lindblad']

    if 'observe' in args:
        observe = args['observe']
    
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
    # ---------------------------------------------------------------------------------------------
    Assert(dt is not None, 'param[\'dt\'] is not set')
    # ---------------------------------------------------------------------------------------------
    print("run starts ...")
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

    # L = operator_L(ro_t, args['lindblad']['out'])
    L_RO = []
    # L_OUT = []
    for i in args['lindblad']['out']:
        L_ = operator_L(ro_t, i)
        L_RO.append(L_)
        # L_OUT.append(L_)

    diag_abs = np.abs(ro_t.data.diagonal(), dtype=np.longdouble)

    sink = {}

    t = 0

    while True:
        diag_abs = np.abs(ro_t.data.diagonal(), dtype=np.longdouble)

        # energy = ro_t.energy(H.capacity, H.cavity.n_atoms,
        #                      H.states_bin, diag_abs)
        # print(np.sum(energy))

        # if sink_list is None:
        #     if np.sum(energy['0_1']) - start_energy['0_1'] > in_photons:
        #         # print("init_energy: ", start_energy, ", energy: ", np.sum(
        #         #     energy[1:]), ", ", np.round(energy, 3), sep="")
        #         # exit(0)
        #         return False
        # -----------------------------------------------------------
        # write
        # writer_all.writerow(["{:.5f}".format(x) for x in diag_abs])
        # writer.writerow(["{:.5f}".format(x) for x in v_bin])

        # if "z_csv" is not None:
        #     writer.writerow(["{:.5f}".format(x) for x in diag_abs])
        # -----------------------------------------------------------
        # T_list
        if T_list is not None:
            T_list.append(t)
        # -----------------------------------------------------------

        if sink_list is not None:
            # zero = diag_abs[0]

            # print(energy['0_1'])
            # exit(0)
            # print(H.states_bin['00'])
            # for k in H.states_bin['00']:
            #     print(H.states[k])
            #     print(diag_abs[k])
            # print(diag_abs[H.states_bin['00']])
            # exit(0)
            # print(diag_abs[H.states_bin['00']])
            # sink[observe] = np.sum(diag_abs[H.states_bin[observe]])
            
            # if __debug__:
            if args['print_all_sink']:
                sink['00'] = np.sum(diag_abs[H.states_bin['00']])
                sink['01'] = np.sum(diag_abs[H.states_bin['01']])
                sink['10'] = np.sum(diag_abs[H.states_bin['10']])
                sink['11'] = np.sum(diag_abs[H.states_bin['11']])
                sink['0_'] = np.sum(diag_abs[H.states_bin['00']])+np.sum(diag_abs[H.states_bin['01']])
                sink['1_'] = np.sum(diag_abs[H.states_bin['10']])+np.sum(diag_abs[H.states_bin['11']])
                sink['_0'] = np.sum(diag_abs[H.states_bin['00']])+np.sum(diag_abs[H.states_bin['10']])
                sink['_1'] = np.sum(diag_abs[H.states_bin['01']])+np.sum(diag_abs[H.states_bin['11']])
                    
                if __debug__:
                    print(np.round([sink['1_'], sink['0_']], 3), sink['1_'] + sink['0_'])
                    # print(np.round([sink['01'], sink['01'], sink['10'], sink['11']], 3))
            # print(np.round(diag_abs, 3))
            # sink['0_1'] = start_energy['0_1'] - \
            #     np.sum(energy['0_1'])
            # sink['1_2'] = start_energy['1_2'] - \
            #     np.sum(energy['1_2'])
            if __debug__:
                # print(sink[observe], 3))
                print(np.round(sink[observe], 3))
                # exit(0)
            sink_list.append(sink[observe])
            # sink_list['1_2'].append(sink['1_2'])  

            # print('dist:', abs(sink_limit - sink['0_1']), abs(sink_limit - sink['1_2']))
            if sink_limit is not None:
                if abs(sink_limit - sink[observe]) < precision: 
                # or \
                   # abs(sink_limit - sink['1_2']) < precision:
                   # print(np.round(diag_abs, 3))
                   # print(sink_limit)
                   # print('ex')
                   return False

            # print(sink['0_1'], sink['1_2'])
        # -----------------------------------------------------------
        for L_OP in L_RO:
            ro_t.data += dt * L_OP(ro_t).data

        ro_t.data = ((U.data).dot(ro_t.data)).dot(U_conj.data)

        Assert(abs(1 - ro_t.abs_trace()) <=
               args['precision'], "ro is not normed: " + str(ro_t.abs_trace()))

        # ro_t.normalize()
        t += dt

    return True
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

# =====================================================================================================================
# def run_out_click(args):
#     # ---------------------------------------------------------------------------------------------
#     ro_0 = args['ro_0'] if 'ro_0' in args else None
#     # print(ro_0.data.diagonal())
#     Assert(ro_0 is not None, 'param[\'ro_0\'] is not set')
#     # ---------------------------------------------------------------------------------------------
#     H = args['H'] if 'H' in args else None

#     Assert(H is not None, 'param[\'H\'] is not set')
#     # ---------------------------------------------------------------------------------------------
#     if 'T_list' in args:
#         T_list = args['T_list']
#         T_list.clear()

#     # if 'sink_list' in args:
#     #     sink_list = args['sink_list']
#     #     sink_list.clear()
#     # ---------------------------------------------------------------------------------------------
#     dt = args['dt'] if 'dt' in args else None

#     Assert(dt is not None, 'param[\'dt\'] is not set')
#     # ---------------------------------------------------------------------------------------------
#     # print("run starts ...")
#     # ---------------------------------------------------------------------------------------------

#     # ---------------------------------------------------------------------------------------------
#     # Unitary
#     U = Unitary(H, dt)

#     # if 'U_csv' in args:
#     #     U.to_csv(args['U_csv'])

#     U_data = U.data

#     U_conj = U.conj()
#     # ---------------------------------------------------------------------------------------------
#     ro_t = ro_0
#     # ---------------------------------------------------------------------------------------------
#     states_dim = []

#     en = 0

#     L_out = operator_L(ro_t, args['lindblad']['out'])

#     diag_abs = np.abs(ro_t.data.diagonal(), dtype=np.longdouble)

#     start_energy = ro_t.energy(
#         H.capacity, H.cavity.n_atoms, H.states_bin, diag_abs)
#     start_energy = np.sum(start_energy)

#     t = 0

#     L_op = L_out

#     L_type = 'out'

#     cnt = 0

#     t_in = 0

#     T_click = []

#     nt = 0
#     p_sink_prev = 0

#     while True:
#         # if t > 0:
#             # print('\t'+time_unit_full(t))
#         # -----------------------------------------------------------
#         ro_t.data = ((U.data).dot(ro_t.data + dt *
#                                   L_op(ro_t).data)).dot(U_conj.data)

#         # ro_t.normalize()

#         # -----------------------------------------------------------
#         # print(L_type)
#         nt += 1
#         t += dt

#         if t >= args['time_limit']:
#             print('t >= time_limit')
#             break

#         diag_abs = np.abs(ro_t.data.diagonal(), dtype=np.longdouble)

#         energy = ro_t.energy(H.capacity, H.cavity.n_atoms,
#                              H.states_bin, diag_abs)
#         if L_type == 'out':
#             p_sink = start_energy - np.sum(energy)
#             # print(p_sink)
#             if nt % args['dt_click'] == 0:
#                 # if nt % 50 == 0:
#                 p_coin = np.random.random_sample()

#                 if p_coin <= p_sink:
#                     # print('p_sink: ', "{:.3f}".format(np.round(
#                     #     p_sink, 3)), ', p_coin: ', "{:.3f}".format(np.round(p_coin, 3)), ' ', time_unit_full(t), sep='')
#                     # print(p_sink, p_coin)
#                     # print(nt, time_unit_full(t))
#                     # exit(0)
#                     return t

#         # -----------------------------------------------------------

#     return cnt


# def run_click(args):
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

#     # if U_csv is not None:
#     #     U.to_csv(args['U_csv'])

#     U_data = U.data

#     U_conj = U.conj()
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

#     ph_out = False

#     T_click = []

#     while True:
#         # for t in range(0, nt+1):
#         # -----------------------------------------------------------
#         # print("\t", t)
#         # print(t, "/", nt)

#         diag_abs = np.abs(ro_t.data.diagonal(), dtype=np.longdouble)
#         # print(diag_abs)
#         energy = ro_t.energy(H.capacity, H.cavity.n_atoms,
#                              H.states_bin, diag_abs)
#         # print(np.sum(energy))

#         p_sink = 1 - np.sum(energy)

#         p_coin = np.random.random_sample()
#         print('p_sink: ', p_sink, ', p_coin: ', p_coin, sep='')

#         if p_coin <= p_sink:
#             T_click.append(t)
#             # ph_out = True
#             break

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
#         ro_t.data = ((U.data).dot(ro_t.data + dt *
#                                   L_ro(ro_t).data)).dot(U_conj.data)

#         Assert(abs(1 - ro_t.abs_trace()) <=
#                args['precision'], "ro is not normed: " + str(ro_t.abs_trace()))

#         # ro_t.normalize()
#         # -----------------------------------------------------------
#         t += dt

#     if ph_out:
#         return True
#     # ---------------------------------------------------------------------------------------------
#     if x_csv is not None:
#         write_x_not_ind(H.states, x_csv)
#     # write_xbp(H.states, config.x_csv, ind=st)

#     if y_csv is not None:
#         write_t(T_str_v(T), nt, y_csv)
#     # ---------------------------------------------------------------------------------------------
#     if z_csv is not None:
#         fz_csv.close()
#     # ---------------------------------------------------------------------------------------------
#     return True
# =====================================================================================================================
