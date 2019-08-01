from PyQuantum.Tools.CSV import *
from PyQuantum.Tools.Assert import *
import plotly.graph_objs as go
import numpy as np
from PyQuantum.Tools.PlotBuilder2D import *


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


data = []

M_str = ''

for w_0 in [
    {
        'name': 's_2',
        'title': '|s<sub>2</sub>〉',
        # 'obj': s_2,
    },
    {
        'name': 't_0',
        'title': '|t<sub>0</sub>〉',
        # 'obj': t_0,
    }
]:
    gamma = []

    M_list = []

    # for coeff in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]:
    # for coeff in list(np.arange(0.01, 10.01, 0.01)):
    # for coeff in list(np.arange(0.01, 1.01, 0.01)):
    # print(list(np.arange(0.01, 1.01, 0.01)) + list(np.arange(10.0, 210.0, 10.0)))

    gamma_list = list(np.arange(4.0, 6.0, 1.0))
    # gamma_list = list(np.arange(0.01, 1.01, 0.01)) + list(np.arange(2.0, 5.0, 1.0))

    gamma_list = np.round(gamma_list, 3)

    print(gamma_list)

    for coeff in gamma_list:
        # for coeff in list(np.arange(0.01, 1.01, 0.01)) + list(np.arange(10.0, 210.0, 10.0)):

        # for coeff in [0.01] + list(range(10.00, 201.00, 10.0)):
        # for coeff in np.arange(10.00, 201.00, 10.0):
        # for coeff in np.arange(0.10, 5.10, 0.10):
        # for coeff in np.arange(0.10, 3.10, 0.10):
        # for coeff in np.arange(0.01, 1.01, 0.01):
        # coeff = np.round(coeff, 3)

        T_list = list_from_csv('MM/M_' + str(coeff) + '/T_' + w_0['name'] + '.csv')
        T_list = np.array(T_list, dtype=np.float64)

        sink_list = list_from_csv('MM/M_' + str(coeff) + '/sink_' + w_0['name'] + '.csv')
        sink_list = np.array(sink_list, dtype=np.float64)

        sink_list /= np.sum(sink_list, dtype=np.float64)

        M = 0

        for i in range(len(T_list)):
            M += sink_list[i] * T_list[i]

        if len(M_list) != 0 and M_list[-1] <= M:
            print(np.sum(sink_list))
            print(sink_list, len(sink_list))
            Assert(M_list[-1] >= M, str(w_0['name']) + ' ' + str(coeff) +
                   ': ' + str(M_list[-1]) + ' < ' + str(M), FILE(), LINE())

        M_list.append(M)
        gamma.append(coeff)

    M_list = np.array(M_list)

    if max(M_list) > 1e6:
        M_list *= 1e-6
        M_str = '10<sup>6</sup>'
        # M_str = '10<sup>6</sup>'
    elif max(M_list) > 1e3:
        M_list *= 1e-3
        M_str = '10<sup>3</sup>'
        # M_str = '10<sup>3</sup>'
    elif max(M_list) > 1e-3:
        M_list *= 1e3
        M_str = 'ms'
        # M_str = '10<sup>-3</sup>'
    elif max(M_list) > 1e-6:
        M_list *= 1e6
        M_str = 'mks'
        # M_str = '10<sup>-6</sup>'
    elif max(M_list) > 1e-9:
        M_list *= 1e9
        M_str = 'ns'
        # M_str = '10<sup>-9</sup>'

    data.append(go.Scatter(
        x=gamma,
        y=M_list,
        name=w_0['title'],
    ))

print("OK")
exit(0)

plot_builder = PlotBuilder2D({
    'title': 'M[p<sub>sink</sub>] (t)',

    'x_title': 'l/g',
    'y_title': 'M, ' + M_str,

    'data': data,

    'to_file': False,

    'html': 'M' + '.html',
    'online': False,
})

plot_builder.make_plot()

# for i in M_list:
# print(i)

# print(l)

# exit(0)

# import matplotlib.pyplot as plt
# import numpy as np

# import plotly.plotly as py
# import plotly.graph_objs as go

# from PyQuantum.Tools.PlotBuilder2D import *

# import plotly

# token = [
#     {
#         'login': 'alexfmsu',
#         'key': 'g8ocp0PgQCY1a2WqBpyr'
#     },
#     {
#         'login': 'alexf-msu',
#         'key': 'VSOCzkhAhdKQDuV7eiYq'
#     },
#     {
#         'login': 'alexfmsu_anime1',
#         'key': 'XvGFBp8VudOGfUBdUxGQ'
#     },
#     {
#         'login': 'alexfmsu_distrib',
#         'key': 'NmiOXaqFkIxx1Ie5BNju'
#     },
#     {
#         'login': 'alexfmsu_movies',
#         'key': '5kV1qs60mmivbVvXNJW6'
#     }
# ]

# token_num = 0

# def change_token():
#     global token_num
#     token_num += 1

#     if token_num >= len(token):
#         print("LIMIT")
#         exit(0)

#     plotly.tools.set_credentials_file(
#         token[token_num]['login'], token[token_num]['key'])

# plotly.tools.set_credentials_file(token[0]['login'], token[0]['key'])

# def df(x, y):
#     f_xn = y[-1]
#     xn = x[-1]

#     DF = []

#     for i in range(len(y)-2, -1, -1):
#         f_xn_1 = y[i]
#         xn_1 = x[i]

#         df = (f_xn-f_xn_1) / (xn - xn_1)
#         # print('i: ', i, ' (', f_xn, '-', f_xn_1, ') / (', xn - xn_1, '), df = ', df, sep='')
#         # print('i: ', i, ', df = ', df, sep='')
#         # print("dx", xn-xn_1)

#         DF.append(df)

#         f_xn = f_xn_1
#         xn = xn_1

#     DF = DF[::-1]

# def df2(x, y):
#     f_xn = y[-1]
#     xn = x[-1]

#     DF = []
#     t = []

#     for i in range(1, len(y)-1):
#         df_ = (y[i+1]-y[i-1]) / (x[i+1] - x[i-1])
#         DF.append(df_)
#         t.append(x[i])
#         # f_xn_1 = y[i]
#         # xn_1 = x[i]

#         # print('i: ', i, ' (', f_xn, '-', f_xn_1, ') / (', xn - xn_1, '), df = ', df, sep='')
#         # print('i: ', i, ', df = ', df, sep='')
#         # print("dx", xn-xn_1)

#         # f_xn = f_xn_1
#         # xn = xn_1

#     return DF, t
#     # DF = DF[::-1]
#     # print(DF[0], DF[-1])
#     # exit(0)
#     # s = 0

#     # for i in range(1, len(DF)):
#     #     s += DF[i] * (x[1]-x[0])
#     # print(s)
#     # print(sum(DF))

#     # return DF

# # for w_0 in ['s_2', 't_0']:
# #     T_list = list_from_csv('T_' + w_0 + '.csv')
# #     sink_list = list_from_csv('sink_' + w_0 + '.csv')

# #     f_xn = sink_list[-1]
# #     xn = T_list[-1]

# #     DF = []

# #     for i in range(len(sink_list)-2, -1, -1):
# #         f_xn_1 = sink_list[i]
# #         xn_1 = T_list[i]

# #         df = (f_xn-f_xn_1) / (xn - xn_1)

# #         DF.append(df)

# #         f_xn = f_xn_1
# #         xn = xn_1

# #     plt.plot(T_list[1:], DF[::-1])
# #     plt.show()
# #     # plt.xlim(0, max_sch)
# #     # plt.ylim(0, 1)

# #     # plt.plot(T_list, sink_list)
# #     # plt.show()

# # for w_0 in ['t_0']:
# # for w_0 in ['s_2']:
# #     # for w_0 in ['s_2', 't_0']:
# #     T_list = list_from_csv('T_' + w_0 + '.csv')
# #     sink_list = list_from_csv('sink_' + w_0 + '.csv')

# #     T = T_list[-1]
# #     T_str = None

# #     if T >= 1e-3:
# #         T_str = 'ms'
# #         T_list = [i * 1e3 for i in T_list]
# #     elif T >= 1e-6:
# #         T_str = 'mks'
# #         T_list = [i * 1e6 for i in T_list]
# #     elif T >= 1e-9:
# #         T_str = 'ns'
# #         T_list = [i * 1e9 for i in T_list]

# #     # plt.ylim(0, 1)

# #     # plt.plot(T_list, sink_list)
# #     # plt.show()

# #     data = [go.Scatter(x=T_list, y=sink_list)]

# #     make_plot({
# #         'to_file': False,
# #         'online': False,
# #         'data': data,
# #         'x_title': 'time, ' + str(T_str),
# #         'y_title': 'sink',
# #         'title': w_0,
# #         'html': w_0 + '.html',
# #     })

# data = []

# # for w_0 in ['t_0']:
# # for w_0 in ['s_2']:

# for w_0 in ['s_2', 't_0']:
#     # for w_0 in ['s_2', 't_0']:
#     T_list = list_from_csv('T_' + w_0 + '.csv')
#     sink_list = list_from_csv('sink_' + w_0 + '.csv')

#     # print(sum(T_list) / len(T_list))
#     # exit(0)
#     # T = T_list[-1]
#     # T_str = None

#     # if T >= 1e-3:
#     #     T_str = 'ms'
#     #     # T_list = [i * 1e3 for i in T_list]
#     # elif T >= 1e-6:
#     #     T_str = 'mks'
#     #     # T_list = [i * 1e6 for i in T_list]
#     # elif T >= 1e-9:
#     #     T_str = 'ns'
#     #     # T_list = [i * 1e9 for i in T_list]

#     # plt.ylim(0, 1)

#     # plt.plot(T_list, sink_list)
#     # plt.show()
#     # T_list
#     # df_ = df(T_list, sink_list)
#     # exit(0)
#     # df_, T_ = df2(T_list, sink_list)
#     # for j in T_:
#     #     print(j)
#     # exit(0)

#     M = 0

#     for i in range(len(T_list)):
#         M += T_list[i] * sink_list[i]

#     print(M)

#     # if w_0 == 's_2':
#     #     data.append(go.Scatter(
#     #         # x=T_list,
#     #         # y=sink_list,
#     #         x=T_,
#     #         y=df_,
#     #         # x=T_list[1:],
#     #         # y=df(T_list, sink_list),
#     #         name='|' + 's2' + '〉',
#     #     ))
#     # else:
#     #     data.append(go.Scatter(
#     #         # x=T_list,
#     #         # y=sink_list,
#     #         x=T_,
#     #         y=df_,
#     #         # x=T_list[1:],
#     #         # y=df(T_list, sink_list),
#     #         name='|' + 't0' + '〉',
#     #     ))
#     # data.append(go.Scatter(
#     #     x=T_list,
#     #     y=sink_list,
#     #     name=w_0,
#     # ))

# # make_plot({
# #     'to_file': False,
# #     'online': False,
# #     'data': data,
# #     'x_title': 'time, ' + str(T_str),
# #     'y_title': 'p_sink',
# #     'title': 'p_sink',
# #     # 'title': w_0,
# #     'html': w_0 + '.html',
# # })

# # make_plot({
# #     'to_file': False,
# #     'online': False,
# #     'data': data,
# #     'x_title': 'time, ' + str(T_str),
# #     'y_title': 'sink',
# #     'y_title': 'dP/dt',
# #     'title': 'dP/dt',
# #     # 'title': w_0,
# #     'html': w_0 + '.html',
# # })
# # })
# # })
# # })
# })
