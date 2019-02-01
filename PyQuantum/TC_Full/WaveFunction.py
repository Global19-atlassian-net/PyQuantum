import numpy as np
from scipy.linalg import expm

import PyQuantum.TC_Full.animator as animator

from PyQuantum.TC_Full.Unitary import *

# import PyQuantum.TC_Full.Hamiltotian as H1
import csv
precision = 5
# precision = config.precision


def get_w0(ph_count, init_state):
    # ------------------------------------------------------------------------------------------------------------------
    # wf_err.get_w0_err(ph_count, init_state)
    # ------------------------------------------------------------------------------------------------------------------
    at = init_state[1]
    at_count = len(at)
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    if init_state[0] > ph_count:
        return -1
    # ------------------------------------------------------------------------------------------------------------------
    ph_state = np.zeros(shape=(ph_count+1, 1))
    ph_state[init_state[0]][0] = 1

    w0 = np.matrix(ph_state)

    for i in range(1, at_count+1):
        at_state = np.zeros(shape=(2, 1))
        if at[i-1] in range(0, 2):
            at_state[at[i-1]][0] = 1
        else:
            return -1

        w0 = np.kron(w0, at_state)

    w0 = np.matrix(w0)
    # ------------------------------------------------------------------------------------------------------------------

    return w0


def get_wdt(wt, exp_iHdt):

    wt = np.dot(exp_iHdt, wt)

    return wt


def get_wt(w0, H, t):
    # wf_err.get_wt_err(w0, H, t)

    exp = expm(np.array(H) * complex(0, -1) * t)

    wt = np.dot(exp, w0)

    return wt


def get_ro(w):
    return np.multiply(w, w.getH())
#######################################################################################################################
# !DONE


def is_hermitian(matrix):
    # wf_err.is_hermitian_err(matrix)

    diff = matrix - matrix.getH()

    return np.all(abs(diff) < precision)
# ----------------------------------------------------------------------------------------------------------------------
# !DONE


def is_unitary(matrix):
    # wf_err.is_unitary_err(matrix)

    matrix_CT = matrix
    diff = matrix * matrix_CT - matrix_CT * matrix

    return np.all(abs(diff) < precision)
#######################################################################################################################


def run(w0, H, t0, t1, initstate, nt=200, not_empty=False, ymin=0, ymax=1, RWA=True, title='title', color='blue'):
    # ------------------------------------------------------------------------------------------------------------------
    if not(nt in range(0, 501)):
        return -1

    nt = 100

    if t0 < 0:
        return -1
    if t1 < 0:
        return -1
    if t0 >= t1:
        return -1

    if len(np.shape(H)) != 2:
        return -1
    if np.shape(H)[0] != np.shape(H)[1]:
        return -1
    if np.shape(H)[0] != len(w0):
        return -1
    # ------------------------------------------------------------------------------------------------------------------
    t = np.linspace(t0, t1, nt+1)

    dt = t[1] - t[0]
    # ------------------------------------------------------------------------------------------------------------------
    state = []

    at_count = len(initstate[1])

    for i in range(0, len(w0)):
        ph_count = int(i / pow(2, at_count))
        st_number = i % pow(2, at_count)

        at_binary = bin(st_number)[2:].zfill(at_count)

        state.append('[' + str(ph_count) + '|' + at_binary + ']')
    # ------------------------------------------------------------------------------------------------------------------
    w = []

    exp_iHdt = expm(np.array(H) * complex(0, -1) * dt)

    wt = w0

    for i in range(0, nt+1):
        wt = get_wdt(wt, exp_iHdt)

        if np.max(wt) > 1:
            sys.exit("Error\n")
        w.append(np.abs(wt))

    w = np.array(w)
    w = w[:, :, 0]
    # ------------------------------------------------------------------------------------------------------------------
    st = initstate[0]*(pow(2, at_count))
    at = 0

    for i in range(0, at_count):
        at += pow(2, i)*initstate[1][at_count-i-1]

    # ------------------------------------------------------------------------------------------------------------------

    return


def Run_RWA(w0, H, t0, t1, initstate, certain_state, config, nt=200, ymin=0, ymax=1, RWA=True, title='title', color='blue'):
    t = np.linspace(t0, t1, nt+1)

    dt = t[1] - t[0]

    # --------------------------------------------------------
    U = Unitary(H, dt)

    if __debug__:
        U.write_to_file(config.U_csv)

    U_conj = U.conj()
    # --------------------------------------------------------
    state = []

    at_count = len(initstate[1])

    for i in range(0, len(w0)):
        ph_count = int(i / pow(2, at_count))
        st_number = i % pow(2, at_count)

        at_binary = bin(st_number)[2:].zfill(at_count)

        state.append('[' + str(ph_count) + '|' + at_binary + ']')
    # ------------------------------------------------------------------------------------------------------------------
    w = []

    w_0 = np.matrix(w0.data)
    w_t = np.array(w0.data)

    wt = w0

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

    # w = w[:, :, 0]
    # ------------------------------------------------------------------------------------------------------------------
    st = certain_state[0]*(pow(2, at_count))
    at = 0

    for i in range(0, at_count):
        at += pow(2, i) * certain_state[1][at_count-i-1]
    # ------------------------------------------------------------------------------------------------------------------
    animator.make_plot(t, t0, t1, ymin, ymax,
                       w[:, st+at], color, title=title, X=r'$t,\ мкс$', Y=r'$Probability$   ')

    return


def run_RWAw(w0, H, t0, t1, initstate, certain_state1, certain_state2, nt=200, ymin=0, ymax=1, RWA=True, title='title', color='blue'):
    # ------------------------------------------------------------------------------------------------------------------
    if not(nt in range(0, 501)):
        return -1

    if t0 < 0:
        return -1
    if t1 < 0:
        return -1
    if t0 >= t1:
        return -1

    if len(np.shape(H)) != 2:
        return -1
    if np.shape(H)[0] != np.shape(H)[1]:
        return -1
    if np.shape(H)[0] != len(w0):
        return -1
    # ------------------------------------------------------------------------------------------------------------------
    nt = t1 * 100

    t = np.linspace(t0, t1, nt+1)

    dt = t[1] - t[0]
    # ------------------------------------------------------------------------------------------------------------------
    state = []

    at_count = len(initstate[1])

    for i in range(0, len(w0)):
        ph_count = int(i / pow(2, at_count))
        st_number = i % pow(2, at_count)

        at_binary = bin(st_number)[2:].zfill(at_count)

        state.append('[' + str(ph_count) + '|' + at_binary + ']')

    st1 = []

    at_count = len(certain_state1[1])

    for i in range(0, len(w0)):
        ph_count = int(i / pow(2, at_count))
        st_number = i % pow(2, at_count)

        at_binary = bin(st_number)[2:].zfill(at_count)

        st1.append('[' + str(ph_count) + '|' + at_binary + ']')

    st2 = []

    at_count = len(certain_state2[1])

    for i in range(0, len(w0)):
        ph_count = int(i / pow(2, at_count))
        st_number = i % pow(2, at_count)

        at_binary = bin(st_number)[2:].zfill(at_count)

        st2.append('[' + str(ph_count) + '|' + at_binary + ']')
    # ------------------------------------------------------------------------------------------------------------------
    w = []

    exp_iHdt = expm(np.array(H) * complex(0, -1) * dt)

    wt = w0

    for i in range(0, nt+1):
        wt = get_wdt(wt, exp_iHdt)

        if np.max(wt) > 1:
            sys.exit("Error\n")
        w.append(np.abs(wt))

    w = np.array(w)
    w = w[:, :, 0]
    # ------------------------------------------------------------------------------------------------------------------
    st1 = certain_state1[0]*(pow(2, at_count))
    at1 = 0

    for i in range(0, at_count):
        at1 += pow(2, i) * certain_state1[1][at_count-i-1]

    st2 = certain_state2[0]*(pow(2, at_count))
    at2 = 0

    for i in range(0, at_count):
        at2 += pow(2, i) * certain_state2[1][at_count-i-1]

    stt1 = str(certain_state1)

    stt2 = str(certain_state2)
    # ------------------------------------------------------------------------------------------------------------------
    animator.make_plot2w(t, t0, t1, ymin, ymax, w[:, st1+at1], w[:, st2+at2], initstate,
                         st1=stt1, st2=stt2, title=title, X=r'$t,\ мкс$', Y=r'$Probability$   ')

    return


def run_EXACT(w0, H, t0, t1, initstate, certain_state, nt=200, ymin=0, ymax=1, title='title', color='blue'):
    # ------------------------------------------------------------------------------------------------------------------
    if not(nt in range(0, 501)):
        return -1

    if t0 < 0:
        return -1
    if t1 < 0:
        return -1
    if t0 >= t1:
        return -1

    # if len(np.shape(H)) != 2: return -1
    # if np.shape(H)[0] != np.shape(H)[1]: return -1
    # if np.shape(H)[0] != len(w0): return -1
    # ------------------------------------------------------------------------------------------------------------------
    nt = t1 * 100

    t = np.linspace(t0, t1, nt+1)

    dt = t[1] - t[0]
    # ------------------------------------------------------------------------------------------------------------------
    state = []

    at_count = len(initstate[1])

    for i in range(0, len(w0)):
        ph_count = int(i / pow(2, at_count))
        st_number = i % pow(2, at_count)

        at_binary = bin(st_number)[2:].zfill(at_count)

        state.append('[' + str(ph_count) + '|' + at_binary + ']')
    # ------------------------------------------------------------------------------------------------------------------
    w = []

    exp_iHdt = expm(np.array(H) * complex(0, -1) * dt)

    wt = w0

    for i in range(0, nt+1):
        wt = get_wdt(wt, exp_iHdt)

        if np.max(wt) > 1:
            sys.exit("Error\n")
        w.append(np.abs(wt))

    w = np.array(w)
    w = w[:, :, 0]
    # #------------------------------------------------------------------------------------------------------------------
    st = certain_state[0]*(pow(2, at_count))
    at = 0

    for i in range(0, at_count):
        at += pow(2, i) * certain_state[1][at_count-i-1]
    # ------------------------------------------------------------------------------------------------------------------
    animator.make_plot(t, t0, t1, ymin, ymax,
                       w[:, st+at], color, title=title, X=r'$t,\ мкс$', Y=r'$Probability$   ')

    return


def run_RWA_3D(w0, H, t0, t1, initstate, nt=200, ymin=0, ymax=1, title='title', color='blue'):
    # ------------------------------------------------------------------------------------------------------------------
    if not(nt in range(0, 501)):
        return -1

    if t0 < 0:
        return -1
    if t1 < 0:
        return -1
    if t0 >= t1:
        return -1

    if len(np.shape(H)) != 2:
        return -1
    if np.shape(H)[0] != np.shape(H)[1]:
        return -1
    if np.shape(H)[0] != len(w0):
        return -1
    # ------------------------------------------------------------------------------------------------------------------
    nt = t1 * 100

    t = np.linspace(t0, t1, nt+1)

    dt = t[1] - t[0]
    # ------------------------------------------------------------------------------------------------------------------
    state = []

    at_count = len(initstate[1])

    for i in range(0, len(w0)):
        ph_count = int(i / pow(2, at_count))
        st_number = i % pow(2, at_count)

        at_binary = bin(st_number)[2:].zfill(at_count)

        state.append('[' + str(ph_count) + '|' + at_binary + ']')
    # ------------------------------------------------------------------------------------------------------------------
    w = []

    exp_iHdt = expm(np.array(H) * complex(0, -1) * dt)

    wt = w0

    for i in range(0, nt+1):
        wt = get_wdt(wt, exp_iHdt)

        if np.max(wt) > 1:
            sys.exit("Error\n")
        w.append(np.abs(wt))
    w = np.array(w)

    w = w[:, :, 0]
    # ------------------------------------------------------------------------------------------------------------------
    st = initstate[0]*(pow(2, at_count))
    at = 0

    for i in range(0, at_count):
        at += pow(2, i)*initstate[1][at_count-i-1]
    # ------------------------------------------------------------------------------------------------------------------
    ww = np.linspace(0, len(w0), len(w0))

    animator.make_plot3D(t, ww, w, state)

    return


def run_EXACT_3D(w0, H, t0, t1, initstate, nt=200, ymin=0, ymax=1, title='title', color='blue'):
    # ------------------------------------------------------------------------------------------------------------------
    if not(nt in range(0, 501)):
        return -1

    if t0 < 0:
        return -1
    if t1 < 0:
        return -1
    if t0 >= t1:
        return -1

    # if len(np.shape(H)) != 2: return -1
    # if np.shape(H)[0] != np.shape(H)[1]: return -1
    # if np.shape(H)[0] != len(w0): return -1
    # ------------------------------------------------------------------------------------------------------------------
    nt = t1 * 100

    t = np.linspace(t0, t1, nt+1)

    dt = t[1] - t[0]
    # ------------------------------------------------------------------------------------------------------------------
    state = []

    at_count = len(initstate[1])

    for i in range(0, len(w0)):
        ph_count = int(i / pow(2, at_count))
        st_number = i % pow(2, at_count)

        at_binary = bin(st_number)[2:].zfill(at_count)

        state.append('[' + str(ph_count) + '|' + at_binary + ']')
    # ------------------------------------------------------------------------------------------------------------------
    w = []

    wt = w0

    exp_iHdt = expm(np.array(H) * complex(0, -1) * dt)

    for i in range(0, nt+1):
        wt = get_wdt(wt, exp_iHdt)

        if np.max(wt) > 1:
            sys.exit("Error\n")
        w.append(np.abs(wt))

    w = np.array(w)

    w = w[:, :, 0]
    # ------------------------------------------------------------------------------------------------------------------
    st = initstate[0]*(pow(2, at_count))
    at = 0

    for i in range(0, at_count):
        at += pow(2, i)*initstate[1][at_count-i-1]
    # ------------------------------------------------------------------------------------------------------------------
    ww = np.linspace(0, len(w0), len(w0))

    animator.make_plot3D(t, ww, w, state)

    return


def run2(w0, H_RWA, H_EXACT, t0, t1, initstate, certain_state, nt=200, ymin=0, ymax=1, title='title'):
    # ------------------------------------------------------------------------------------------------------------------
    if not(nt in range(0, 501)):
        return -1

    if t0 < 0:
        return -1
    if t1 < 0:
        return -1
    if t0 >= t1:
        return -1

    if len(np.shape(H_RWA)) != 2:
        return -1
    if np.shape(H_RWA)[0] != np.shape(H_RWA)[1]:
        return -1
    if np.shape(H_RWA)[0] != len(w0):
        return -1

    if len(np.shape(H_EXACT)) != 2:
        return -1
    if np.shape(H_EXACT)[0] != np.shape(H_EXACT)[1]:
        return -1
    if np.shape(H_EXACT)[0] != len(w0):
        return -1
    # ------------------------------------------------------------------------------------------------------------------
    nt = t1 * 100

    t = np.linspace(t0, t1, nt+1)

    dt = t[1] - t[0]
    # ------------------------------------------------------------------------------------------------------------------
    state = []

    at_count = len(initstate[1])

    for i in range(0, len(w0)):
        ph_count = int(i / pow(2, at_count))
        st_number = i % pow(2, at_count)

        at_binary = bin(st_number)[2:].zfill(at_count)

        state.append('[' + str(ph_count) + '|' + at_binary + ']')
    # ------------------------------------------------------------------------------------------------------------------
    w_RWA = []
    w_EXACT = []

    exp_iHdt_RWA = expm(np.array(H_RWA) * complex(0, -1) * dt)
    exp_iHdt_EXACT = expm(np.array(H_EXACT) * complex(0, -1) * dt)

    wt_RWA = w0
    wt_EXACT = w0

    for i in range(0, nt+1):
        wt_RWA = get_wdt(wt_RWA, exp_iHdt_RWA)
        wt_EXACT = get_wdt(wt_EXACT, exp_iHdt_EXACT)

        if np.max(wt_RWA) > 1 or np.max(wt_EXACT) > 1:
            sys.exit("Error\n")

        w_RWA.append(np.abs(wt_RWA))
        w_EXACT.append(np.abs(wt_EXACT))

    w_RWA = np.array(w_RWA)
    w_EXACT = np.array(w_EXACT)
    # ------------------------------------------------------------------------------------------------------------------
    st = certain_state[0]*(pow(2, at_count))
    at = 0

    for i in range(0, at_count):
        at += pow(2, i) * certain_state[1][at_count-i-1]
    # ------------------------------------------------------------------------------------------------------------------
    animator.make_plot2(t, t0, t1, ymin, ymax,
                        w_RWA[:, st+at], w_EXACT[:, st+at], title, X=r'$t,\ мкс$', Y=r'$Probability$   ')

    return


def run2c(w0, H_RWA, H_EXACT, t0, t1, initstate, certain_state, nt=200, not_empty=False, ymin=0, ymax=1, title='title'):
    # ------------------------------------------------------------------------------------------------------------------
    if not(nt in range(0, 501)):
        return -1

    if t0 < 0:
        return -1
    if t1 < 0:
        return -1
    if t0 >= t1:
        return -1

    if len(np.shape(H_RWA)) != 2:
        return -1
    if np.shape(H_RWA)[0] != np.shape(H_RWA)[1]:
        return -1
    if np.shape(H_RWA)[0] != len(w0):
        return -1

    if len(np.shape(H_EXACT)) != 2:
        return -1
    if np.shape(H_EXACT)[0] != np.shape(H_EXACT)[1]:
        return -1
    if np.shape(H_EXACT)[0] != len(w0):
        return -1
    # ------------------------------------------------------------------------------------------------------------------
    nt = t1 * 100

    t = np.linspace(t0, t1, nt+1)

    dt = t[1] - t[0]
    # ------------------------------------------------------------------------------------------------------------------
    state = []

    at_count = len(initstate[1])

    for i in range(0, len(w0)):
        ph_count = int(i / pow(2, at_count))
        st_number = i % pow(2, at_count)

        at_binary = bin(st_number)[2:].zfill(at_count)

        state.append('[' + str(ph_count) + '|' + at_binary + ']')
    # ------------------------------------------------------------------------------------------------------------------
    w_RWA = []
    w_EXACT = []

    exp_iHdt_RWA = expm(np.array(H_RWA) * complex(0, -1) * dt)
    exp_iHdt_EXACT = expm(np.array(H_EXACT) * complex(0, -1) * dt)

    wt_RWA = w0
    wt_EXACT = w0

    for i in range(0, nt+1):
        wt_RWA = get_wdt(wt_RWA, exp_iHdt_RWA)
        wt_EXACT = get_wdt(wt_EXACT, exp_iHdt_EXACT)

        if np.max(wt_RWA) > 1 or np.max(wt_EXACT) > 1:
            sys.exit("Error\n")

        w_RWA.append(np.abs(wt_RWA))
        w_EXACT.append(np.abs(wt_EXACT))

    w_RWA = np.array(w_RWA)
    w_EXACT = np.array(w_EXACT)
    # ------------------------------------------------------------------------------------------------------------------
    st = certain_state[0]*(pow(2, at_count))
    at = 0

    for i in range(0, at_count):
        at += pow(2, i) * certain_state[1][at_count-i-1]
    # ------------------------------------------------------------------------------------------------------------------
    animator.make_plot2(t, t0, t1, ymin, ymax,
                        w_RWA[:, st+at], w_EXACT[:, st+at], title, X=r'$t,\ мкс$', Y=r'$Probability$   ')

    return


def diff(obj):
    global RWA

    ph_count = int(obj.ph_count.text())
    at_count = int(obj.at_count.text())

    wc = float(obj.wc.text())
    wa = float(obj.wa.text())
    g = float(obj.g.text())

    certain_state = None

    if obj.chk_certain.isChecked():
        at_list = []

        for i in range(0, at_c+1):
            at_list.append(int(c_atoms[i].currentText()))

        certain_state = [int(c_spinbox.text()), at_list]

    at_list = []

    for i in range(0, at_c+1):
        at_list.append(int(atoms[i].currentText()))

        init_state = [int(obj.init_ph_count.text()), at_list]

    w0 = wf.get_w0(ph_count=ph_count, init_state=init_state)

    t = int(obj.t1.text())

    color = ''
    title = ''

    if RWA and not EXACT:
        color = 'blue'
        title += r'$RWA$'+'\n'
    elif not RWA and EXACT:
        color = 'red'
        title += r'$Exact$' + ' ' + r'$solution$'+'\n'
    elif RWA and EXACT:
        title += r'$RWA\ vs\ Exact$'+'\n'

    title += r'$w_c =  ' + str(wc) + '\ МГц,$   ' + r'$w_a = ' + \
        str(wa) + '\ МГц,$   ' + r'$g = ' + str(g) + '\ c^{-1}$'

    H_RWA = H1.get_H(ph_count, at_count, wc, wa, g, RWA=True)
    H_EXACT = H1.get_H(ph_count, at_count, wc, wa, g, RWA=False)

    wt_RWA = get_wt(w0, H_RWA, t)

    return
