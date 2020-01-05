# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Tools
from PyQuantum.Tools.CSV import *
from PyQuantum.Tools.PlotBuilder2D import *
from PyQuantum.Tools.Units import time_unit
from PyQuantum.Tools.Pickle import *
from PyQuantum.Tools.df_dx import *
# ---------------------------------------------------------------------------------------------------------------------
# scientific
import plotly.graph_objs as go
import numpy as np
# ---------------------------------------------------------------------------------------------------------------------

data = []

path = 'sink/1ms_l001g'


def M(p, x):
    m = 0

    for i in range(len(p)):
        m += p[i] * x[i]

    # m /= np.sum(p)

    return m, m / np.sum(p)


for w_0 in ['s2', 't0']:
    T_list = pickle_load(path+'/T_list_' + w_0 + '.pkl')

    sink_list = pickle_load(path+'/sink_list_' + w_0 + '.pkl')
    # sink_list /= np.sum(sink_list)

    T = T_list[-1]
    T_str = None

    T_str = time_unit(T)

    if T >= 1e-3:
        T_list = [i * 1e3 for i in T_list]
    elif T >= 1e-6:
        T_list = [i * 1e6 for i in T_list]
    elif T >= 1e-9:
        T_list = [i * 1e9 for i in T_list]

    if w_0 == 's2':
        pass
    else:
        s = []
        p = []

        for i in range(1, len(T_list)):
            d = np.round(T_list[i], 3) / 0.5

            if int(d) == d:
                # print(str(np.round(T_list[i], 3)) + ' ' + T_str)
                s.append(T_list[i])
                p.append(sink_list[i])

        # p /= np.sum(p)
        # p, s = df2(s, p)

        P = []

        q = 1

        x = list(range(1, len(p)))

        for i in x:
            P.append(p[i] * q)
            q *= 1 - p[i]

        print(p[1:])
        print()
        print(np.round(P, 3))
        print()
        print(x)
        # ss /= np.sum(p)

        print(M(P, x))
