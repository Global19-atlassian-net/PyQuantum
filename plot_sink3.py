# ---------------------------------------------------------------------------------------------------------------------
# scientific
import plotly.graph_objs as go
import numpy as np
# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Tools
from PyQuantum.Tools.CSV import *
from PyQuantum.Tools.PlotBuilder2D import *
from PyQuantum.Tools.Units import time_unit
from PyQuantum.Tools.Pickle import *
# from PyQuantum.Tools.df_dx import *
# ---------------------------------------------------------------------------------------------------------------------

data = []

path = 'sink3/1ms_l001g'
# path = 'sink/1ms_l001g'

for w_0 in ['t_11_000']:
    # for w_0 in ['s2', 't0']:
    T_list = pickle_load(path+'/T_list_' + w_0 + '.pkl')
    # T_list = T_list
    # print(T_list)
    # exit()
    # T_list = list_from_csv('MM/M_' + str(coeff) + '/T_' + w_0 + '.csv')
    # T_list = np.array(T_list)
    # T_list *= 1e-9
    # T_list = [i * 1e-9 for i in ]
    # print(T_list)
    # exit(0)
    # T_list = list_from_csv(pa'T_' + w_0 + '.csv')
    # sink_list = list_from_csv('sink_' + w_0 + '.csv')
    sink_list_01 = pickle_load(path+'/sink_list_' + w_0 + '_01.pkl')
    sink_list_12 = pickle_load(path+'/sink_list_' + w_0 + '_12.pkl')
    # sink_list /= np.sum(sink_list)
    # sink_list = list_from_csv('MM/M_' + str(coeff) + '/sink_' + w_0 + '.csv')

    # print(sum(T_list) / len(T_list))
    # exit(0)
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
        # data.append(go.Scatter(
        #     x=T_list,
        #     y=np.round(sink_list, 3),
        #     # x=T_,
        #     # y=df_,
        #     # x=T_list[1:],
        #     # y=df(T_list, sink_list),
        #     # name='|' + 's' + sub(2) + '〉'
        #     name='<b>|' + 's' + sub(2) + '〉</b>'
        #     # + \
        #     # sub('l = ' + str(coeff) + ' * g'),
        # ))
    else:
        pass
        # print(T_list)
        s = []
        p = []

        # print(T_list)

        # for i in range(len(T_list)):
        #     d = np.round(T_list[i], 3) / 0.01
        #     # print(int(d) == d)
        #     # print(T_list[i])

        #     if int(d) == d:
        #         print(T_list[i])
        #         s.append(T_list[i])
        #         p.append(sink_list[i])

        # ss = 0
        # for i in range(len(s)):
        #     ss += T_list[i] * sink_list[i]
        # ss /= len(s)

        # print(ss)

        # print(i)
        # if np.round(i, 3) / 0.01 == 0:
        # data.append(go.Scatter(
        #     x=T_list,
        #     y=np.round(sink_list, 3),
        #     # x=T_,
        #     # y=df_,
        #     # x=T_list[1:],
        #     # y=df(T_list, sink_list),
        #     # name='|' + 't' + sub(0) + '〉'
        #     name='<b>|' + 't' + sub(0) + '〉'+'</b>'
        #     # + \
        #     # sub('l = ' + str(coeff) + ' * g'),
        # ))
    data.append(go.Scatter(
        x=T_list,
        y=np.round(sink_list_01, 3),
        name='<b>' + '|1⟩|1⟩|000⟩' + sub('01') + '</b>'
    ))
    data.append(go.Scatter(
        x=T_list,
        y=np.round(sink_list_12, 3),

        name='<b>' + '|1⟩|1⟩|000⟩' + sub('12') + '</b>'
    ))
    # data.append(go.Scatter(
    #     x=T_list,
    #     y=sink_list,
    #     name=w_0,
    # ))

# print(data)
# exit(0)

plot_builder = PlotBuilder2D({
    'to_file': False,
    'online': False,
    'data': data,
    'x_title': 't, ' + T_str,
    # 'x_title': 'time, ' + str(T_str),
    'y_title': 'p' + sub('sink'),
    # 'y_title': 'dP/dt',
    'title': 'p' + sub('sink') + '(t)',
    # 'title': 'dP/dt',
    # 'title': w_0,
    'html': 'sink' + '.html',
    'as_annotation': True,
    # 'html': w_0 + '.html',
})

plot_builder.make_plot()

# =====================================================================================================================
