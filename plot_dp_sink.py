# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Tools
from PyQuantum.Tools.CSV import *
from PyQuantum.Tools.PlotBuilder2D import *
from PyQuantum.Tools.Units import time_unit
from PyQuantum.Tools.Pickle import *
# from PyQuantum.Tools.df_dx import *
# ---------------------------------------------------------------------------------------------------------------------
# scientific
import plotly.graph_objs as go
import numpy as np
# ---------------------------------------------------------------------------------------------------------------------


data = []

# for w_0 in ['t_0']:
# for w_0 in ['s_2']:

gamma_list = [1]
# gamma_list = list(np.arange(4.0, 6.0, 1.0))

path = 'sink/1ms_l001g'


def df2(x, y):
    f_xn = y[-1]
    xn = x[-1]

    DF = []
    t = []

    for i in range(1, len(y)-1):
        df_ = (y[i+1]-y[i-1]) / (x[i+1] - x[i-1])
        DF.append(df_)
        t.append(x[i])

    return DF, t


y_max = 0

for coeff in gamma_list:
    # path = 'M_' + str(np.round(coeff, 3))

    # for w_0 in ['t_0']:
    for w_0 in ['t0', 's2']:

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
        sink_list = pickle_load(path+'/sink_list_' + w_0 + '.pkl')
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

        df_, T_ = df2(T_list, sink_list)

        y_max = max(y_max, max(df_))

        if w_0 == 's2':
            data.append(go.Scatter(
                x=np.round(T_, 3),
                y=np.round(df_, 3),
                # x=T_,
                # y=df_,
                # x=T_list[1:],
                # y=df(T_list, sink_list),
                # name='|' + 's' + sub(2) + '〉'
                name='<b>|' + 's' + sub(2) + '〉</b>'
                # + \
                # sub('l = ' + str(coeff) + ' * g'),
            ))
        else:
            data.append(go.Scatter(
                x=np.round(T_, 3),
                y=np.round(df_, 3),
                # x=T_,
                # y=df_,
                # x=T_list[1:],
                # y=df(T_list, sink_list),
                # name='|' + 't' + sub(0) + '〉'
                name='<b>|' + 't' + sub(0) + '〉'+'</b>'
                # + \
                # sub('l = ' + str(coeff) + ' * g'),
            ))
        # data.append(go.Scatter(
        #     x=T_list,
        #     y=sink_list,
        #     name=w_0,
        # ))


print(data)
# print(y_max)
# exit(0)

plot_builder = PlotBuilder2D({
    'to_file': False,
    'online': False,
    'data': data,
    'y_range': [0, 1],
    # 'y_range': [0, np.round(y_max, 3)],
    'x_title': 't, ' + T_str,
    # 'x_title': 'time, ' + str(T_str),
    'y_title': 'dP/dt',
    # 'y_title': 'dP/dt',
    'title': 'dP/dt',
    # 'title': 'dP/dt',
    # 'title': w_0,
    'html': 'dp_dt' + '.html',
    'as_annotation': True,
    # 'html': w_0 + '.html',
})

plot_builder.make_plot()

# =====================================================================================================================
# plt.ylim(0, 1)

# plt.plot(T_list, sink_list)
# plt.show()

# df_ = df(T_list, sink_list)

# df_, T_ = df2(T_list, sink_list)

# for j in T_:
#     print(j)
# =====================================================================================================================
# for w_0 in ['s_2', 't_0']:
#     T_list = list_from_csv('T_' + w_0 + '.csv')
#     sink_list = list_from_csv('sink_' + w_0 + '.csv')

#     f_xn = sink_list[-1]
#     xn = T_list[-1]

#     DF = []

#     for i in range(len(sink_list)-2, -1, -1):
#         f_xn_1 = sink_list[i]
#         xn_1 = T_list[i]

#         df = (f_xn-f_xn_1) / (xn - xn_1)

#         DF.append(df)

#         f_xn = f_xn_1
#         xn = xn_1

#     plt.plot(T_list[1:], DF[::-1])
#     plt.show()
#     # plt.xlim(0, max_sch)
#     # plt.ylim(0, 1)

#     # plt.plot(T_list, sink_list)
#     # plt.show()

# for w_0 in ['t_0']:
# for w_0 in ['s_2']:
#     # for w_0 in ['s_2', 't_0']:
#     T_list = list_from_csv('T_' + w_0 + '.csv')
#     sink_list = list_from_csv('sink_' + w_0 + '.csv')

#     T = T_list[-1]
#     T_str = None

#     if T >= 1e-3:
#         T_str = 'ms'
#         T_list = [i * 1e3 for i in T_list]
#     elif T >= 1e-6:
#         T_str = 'mks'
#         T_list = [i * 1e6 for i in T_list]
#     elif T >= 1e-9:
#         T_str = 'ns'
#         T_list = [i * 1e9 for i in T_list]

#     # plt.ylim(0, 1)

#     # plt.plot(T_list, sink_list)
#     # plt.show()

#     data = [go.Scatter(x=T_list, y=sink_list)]

#     make_plot({
#         'to_file': False,
#         'online': False,
#         'data': data,
#         'x_title': 'time, ' + str(T_str),
#         'y_title': 'sink',
#         'title': w_0,
#         'html': w_0 + '.html',
#     })
# =====================================================================================================================
