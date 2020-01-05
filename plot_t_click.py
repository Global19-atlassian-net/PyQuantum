# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Tools
from PyQuantum.Tools.Assert import *
from PyQuantum.Tools.CSV import *
from PyQuantum.Tools.PlotBuilder2D import *
from PyQuantum.Tools.Units import time_unit
from PyQuantum.Tools.Pickle import *
# from PyQuantum.Tools.df_dx import *
# ---------------------------------------------------------------------------------------------------------------------
# scientific
import plotly.graph_objs as go
import numpy as np
from math import sqrt, pi
# ---------------------------------------------------------------------------------------------------------------------


def gauss(x, sigma, x0):
    return 1.0/(sigma*sqrt(2*pi)) * np.exp(-(x-x0)**2 / (2*sigma**2))


data = []

gamma_list = [1]


NP = 500
dt = 1000
nt_batch = 20

path = 'T_click/l1g/' + str(dt) + 'ns/'

for w_0 in ['t0', 's2']:
    # for w_0 in ['s2', 't0']:
    # ---------------------------------------------------------------------------------------------
    T_list = []

    for i in range(NP):
        T_ = pickle_load(path+'/' + w_0 + '/' + str(i) + '.pkl')
        # T_ = pickle_load(path+'/'+w_0 + '_' + str(i) + '.pkl')
        T_list += T_

    print(len(T_list))
    # exit(0)
    Assert(len(T_list) == NP * nt_batch, 'len(T_list) != np * 10')

    # T = T_list[-1]

    # T_str = None

    # T_str = time_unit(T)

    # if T >= 1e-3:
    #     T_list = [i * 1e3 for i in T_list]
    # elif T >= 1e-6:
    #     T_list = [i * 1e6 for i in T_list]
    # elif T >= 1e-9:
    #     T_list = [i * 1e9 for i in T_list]
    T_list = [i * 1e9 for i in T_list]

    # print(T_list)

    T_min = round(min(T_list))
    T_max = round(max(T_list))
    print(T_min, T_max)
    # ---------------------------------------------------------------------------------------------
    T_list = np.round(T_list)
    print(T_list)
    # ---------------------------------------------------------------------------------------------
    print(int((T_max-T_min) / dt))
    n = np.zeros(int((T_max) / dt + 1))
    # n = np.zeros(int((T_max-T_min) / dt + 1))

    print('n:', n)

    for t in T_list:
        # print(t, t/dt, int(t/dt)-int(T_min/dt))
        n[int(t / dt)] += 1
        # n[int(t / dt) - int(T_min/dt)] += 1
        # print(t)
    print(n)
    # exit(0)
    Assert(np.sum(n) == NP * nt_batch, 'np.sum(n) == np * nt_batch')
    # ---------------------------------------------------------------------------------------------

    # if w_0 == 's2':
    #     data.append(go.Scatter(
    #         x=T_list,
    #         y=n,
    #         # y=np.round(sink_list, 3),
    #         # x=T_,
    #         # y=df_,
    #         # x=T_list[1:],
    #         # y=df(T_list, sink_list),
    #         # name='|' + 's' + sub(2) + '〉'
    #         name='<b>|' + 's' + sub(2) + '〉</b>'
    #         # + \
    #         # sub('l = ' + str(coeff) + ' * g'),
    #     ))
    # else:
    #     data.append(go.Scatter(
    #         x=T_list,
    #         y=n,
    #         # x=T_,
    #         # y=df_,
    #         # x=T_list[1:],
    #         # y=df(T_list, sink_list),
    #         # name='|' + 't' + sub(0) + '〉'
    #         name='<b>|' + 't' + sub(0) + '〉'+'</b>'
    #         # + \
    #         # sub('l = ' + str(coeff) + ' * g'),
    #     ))
    # print(n)
    # exit(0)
    # n /= np.sum(n)
    if w_0 == 's2':
        data.append(go.Scatter(
            x=list(range(0, T_max+1, dt)),
            y=n,
            name='<b>|' + 's' + sub(2) + '〉'+'</b>',
        ))
    elif w_0 == 't0':
        data.append(go.Scatter(
            x=list(range(0, T_max+1, dt)),
            y=n,
            name='<b>|' + 't' + sub(0) + '〉'+'</b>',
        ))
    # x = list(range(T_min, T_max+1, dt))

    # data.append(go.Scatter(
    #     x=list(range(T_min, T_max+1, dt)),
    #     y=gauss(x, sigma=1.0/sqrt(len(T_list)), x0=np.sum(x)/len(x)),
    #     name=w_0,
    # ))

# print(data)
# # exit(0)

plot_builder = PlotBuilder2D({
    'to_file': False,
    'online': False,
    'data': data,
    'x_title': 't, ns',
    # 'x_title': 'time, ' + str(T_str),
    'y_title': r'N',
    # 'y_title': 'p' + sub('sink'),
    # 'y_title': 'dP/dt',
    'title': 'N(t),        T' + sub('click') + ' = ' + str(dt) + ' ns',
    # 'title': 'dP/dt',
    # 'title': w_0,
    'html': 'sink' + '.html',
    'as_annotation': True,
    'y_range': [0, 1700]
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
