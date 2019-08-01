from PyQuantum.Tools.PlotBuilder2D import *
from PyQuantum.Tools.CSV import *

import numpy as np

x = []
y = []

path = 'oout'
# path = 'out_2'

count = 99

for i in range(count+1):
    Fidelity_s2_list = list_from_csv(path+'/fidelity_s2' + str(i) + '.csv')
    T_list = list_from_csv(path+'/T_list' + str(i) + '.csv')
    cnt = list_from_csv(path+'/cnt' + str(i) + '.csv')

    # print(T_list)

    T_out = T_list[0]

    for t in range(1, len(T_list)):
        T_out += T_list[t] - T_list[t-1]

    # T_avg = T_out
    T_out /= cnt[0]

    T_avg = sum([t for t in T_list]) / cnt[0]

    # print(i, ': ', T_sum, ', ', cnt, sep='')
    T_str = None

    if max(T_list) >= 1e-3:
        T_str = 'ms'
        T_avg *= 1e3
        T_out *= 1e3
        # T_list = [i * 1e3 for i in T_list]
    elif max(T_list) >= 1e-6:
        T_str = 'mks'
        T_avg *= 1e6
        T_out *= 1e6

        # T_list = [i * 1e6 for i in T_list]
    elif max(T_list) >= 1e-9:
        T_str = 'ns'
        T_avg *= 1e9
        T_out *= 1e9

        # T_list = [i * 1e9 for i in T_list]

    # print(Fidelity_s2_list[0], T_out)
    y.append(T_avg)
    x.append(T_out)

    # x.append(Fidelity_s2_list[0])
    # x.append(i)
    # y.append(T_out)


# print(x)
# print(y)
# exit(0)

data = [go.Scatter(
    x=x,
    y=y,
    mode='markers',
    # x=T_list[1:],
    # y=df(T_list, sink_list),
    # name=w_0,
)]

make_plot({
    'to_file': False,
    'online': False,
    'data': data,
    'x_title': 'time, ' + str(T_str),
    'y_title': 'sink',
    'title': 'avg',
    'html': 'avg.html',
})
