from PyQuantum.Tools.PlotBuilder2D import *
from PyQuantum.Tools.CSV import *

import numpy as np

x = []
y = []

# path = 'oout'
path = 'out_2'


def df(x, y):
    f_xn = y[-1]
    xn = x[-1]

    DF = []

    for i in range(len(y)-2, -1, -1):
        f_xn_1 = y[i]
        xn_1 = x[i]

        df = (f_xn-f_xn_1) / (xn - xn_1)

        DF.append(df)

        f_xn = f_xn_1
        xn = xn_1

    return DF[::-1]


n_counts = 100

for i in range(1, 2):
    # Fidelity_s2_list = list_from_csv(path+'/fidelity_s2' + str(i) + '.csv')
    T_list = list_from_csv(path+'/T_list' + str(i) + '.csv')
    cnt = list_from_csv(path+'/cnt' + str(i) + '.csv')

    print(len(T_list))
    # print(T_list)
    Tt = [T_list[0]]

    # for i in T_list:
    #     print(i)
    # exit(0)
    for t in range(1, len(T_list)):
        Tt.append(T_list[t] - T_list[t-1])
        # print(T_list[t], '-', T_list[t-1], T_list[t] - T_list[t-1])

    dt_avg = sum(Tt) / cnt[0]

    print(dt_avg)
    exit(0)
    for i in Tt:
        print(i * 1e9)

    exit(0)
    # # dt /= cnt[0]

    # print(dt)

    # dt_avg = sum(dt) / cnt[0]

    dt = max(Tt) / n_counts

    Ti = []

    for j in range(n_counts+1):
        Ti.append(dt * j)

    print(Ti)

    Ni = [0] * (n_counts+1)

    for j in Tt:
        print(j, dt, int(j / dt))
        Ni[int(j / dt)] += 1

    print(Ni)

    y = Ni
    x = Ti
    # exit(0)
    # y = df(T_list, sink_list)
    # x = dt_avg
    # exit(0)
    # T_avg = sum([t for t in T_list]) / cnt[0]

    # # print(i, ': ', T_sum, ', ', cnt, sep='')
    # T_str = None

    if max(T_list) >= 1e-3:
        # Ti *= 1e3
        #     T_str = 'ms'
        #     T_avg *= 1e3
        #     dt *= 1e3
        # T_list = [i * 1e3 for i in T_list]
        Ti = [i * 1e3 for i in Ti]

    elif max(T_list) >= 1e-6:
        # Ti *= 1e6
        #     T_str = 'mks'
        #     T_avg *= 1e6
        #     dt *= 1e6
        #     T_list = [i * 1e6 for i in T_list]
        Ti = [i * 1e6 for i in Ti]

    elif max(T_list) >= 1e-9:
        Ti = [i * 1e9 for i in Ti]
        # Ti *= 1e9
    #     T_str = 'ns'
    #     T_avg *= 1e9
    #     dt *= 1e9
    #     # T_list *= 1e9
    #     T_list = [i * 1e9 for i in T_list]

    #     # T_list = [i * 1e9 for i in T_list]

    # # print(Fidelity_s2_list[0], dt)
    # # x = list(range(1, cnt[0]+1))
    # # y = T_list
    # # x =
    # y = df(T_list)
    # x.append(Fidelity_s2_list[0])
    # x.append(i)
    # y.append(dt)


print(x, len(x))
print(y, len(y))
exit(0)

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
    'x_title': 'time, ' + '',
    # 'x_title': 'time, ' + str(T_str),
    'y_title': 'sink',
    'title': 'avg',
    'html': 'avg.html',
})
