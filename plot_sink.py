# ---------------------------------------------------------------------------------------------------------------------
# PyQuantum.Tools
from PyQuantum.Tools.CSV import *
from PyQuantum.Tools.PlotBuilder2D import *
from PyQuantum.Tools.Units import time_unit, time_unit_full
from PyQuantum.Tools.Pickle import *
# from PyQuantum.Tools.df_dx import *
# ---------------------------------------------------------------------------------------------------------------------
# scientific
import plotly.graph_objs as go
import numpy as np
# ---------------------------------------------------------------------------------------------------------------------

data = []

# path = 'sink3/0_1ms_1ns_l001g_l001g'
# path = 'sink/1ms_l001g'

w_0_name = {}
# w_0_name['11_000'] = '<b>|0' + sub(1) + '0' + sub(2) + '0' + sub(3) + '〉'+'</b>'
# # w_0_name['11_000'] = '<b>|000' + '〉'+'</b>'
# w_0_name['11_0D'] = '<b>|0' + sub(1) +'〉' + '( |0' + sub(2) + '1' + sub(3) + '〉- |1'+sub(2)+'0'+sub(3)+'〉'+')</b>'
# w_0_name['11_1D'] = '<b>|0' + sub(2) +'〉' + '( |0' + sub(1) + '1' + sub(3) + '〉- |1'+sub(1)+'0'+sub(3)+'〉'+')</b>'
# w_0_name['11_2D'] = '<b>|0' + sub(3) +'〉' + '( |0' + sub(1) + '1' + sub(2) + '〉- |1'+sub(1)+'0'+sub(2)+'〉'+')</b>'
# w_0_name['11_D'] = '<b>|D' + sub(3) +'〉'+ '</b>'

# path = 'sink3/1_1ms_01ns_l5g_l5g'
# w_0_name['10_000'] = '<b>|0' + sub(1) + '0' + sub(2) + '0' + sub(3) + '〉'+'</b>'
# # w_0_name['11_000'] = '<b>|000' + '〉'+'</b>'
# w_0_name['10_0D'] = '<b>|0' + sub(1) +'〉' + '( |0' + sub(2) + '1' + sub(3) + '〉- |1'+sub(2)+'0'+sub(3)+'〉'+')</b>'
# w_0_name['10_1D'] = '<b>|0' + sub(2) +'〉' + '( |0' + sub(1) + '1' + sub(3) + '〉- |1'+sub(1)+'0'+sub(3)+'〉'+')</b>'
# w_0_name['10_2D'] = '<b>|0' + sub(3) +'〉' + '( |0' + sub(1) + '1' + sub(2) + '〉- |1'+sub(1)+'0'+sub(2)+'〉'+')</b>'
# w_0_name['10_D'] = '<b>|D' + sub(3) +'〉'+ '</b>'

path = 'sink3/1_1ms_01ns_l01g_l01g'
w_0_name['01_000'] = '<b>|0' + sub(1) + '0' + sub(2) + '0' + sub(3) + '〉'+'</b>'
# w_0_name['11_000'] = '<b>|000' + '〉'+'</b>'
w_0_name['01_0D'] = '<b>|0' + sub(1) +'〉' + '( |0' + sub(2) + '1' + sub(3) + '〉- |1'+sub(2)+'0'+sub(3)+'〉'+')</b>'
w_0_name['01_1D'] = '<b>|0' + sub(2) +'〉' + '( |0' + sub(1) + '1' + sub(3) + '〉- |1'+sub(1)+'0'+sub(3)+'〉'+')</b>'
w_0_name['01_2D'] = '<b>|0' + sub(3) +'〉' + '( |0' + sub(1) + '1' + sub(2) + '〉- |1'+sub(1)+'0'+sub(2)+'〉'+')</b>'
w_0_name['01_D'] = '<b>|D' + sub(3) +'〉'+ '</b>'

# for w_0 in ['11_000', '11_0D', '11_1D', '11_2D', '11_D']:
# for w_0 in ['10_000', '10_0D', '10_1D', '10_2D', '10_D']:
for w_0 in ['01_000', '01_0D', '01_1D', '01_2D', '01_D']:
# for w_0 in ['11_D']:
# for w_0 in ['t_11_000']:
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
    sink_list = pickle_load(path+'/sink_list_' + w_0 + '.pkl')
    print(time_unit_full(max(T_list)))
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

    # if w_0 == 's2':
        # pass
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
    # else:
        # print(T_list)
        # s = []
        # p = []

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
        # print('ex')
        # exit(0)
    data.append(go.Scatter(
        x=T_list,
        y=np.round(sink_list, 3),
            # x=T_,
            # y=df_,
            # x=T_list[1:],
            # y=df(T_list, sink_list),
            # name='|' + 't' + sub(0) + '〉'
            # name='<b>|000' + '〉'+'</b>'
        name=w_0_name[w_0],
            # name='<b>|' + 't' + sub(0) + '〉'+'</b>'
            # + \
            # sub('l = ' + str(coeff) + ' * g'),
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
