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
from math import sqrt, pi, log2
# ---------------------------------------------------------------------------------------------------------------------


def gauss(x, sigma, x0):
    x = np.array(x)

    return 1.0/(sigma*sqrt(2*pi)) * np.exp((-(x-x0)**2) / (2*sigma**2))


plot_data = []

gamma_list = [1]


epoch = 10
epoch_size = 100
# dt = 50
# dt = 100
# dt = 250
dt = 100

# M = log2()
dt_avg = 1
# dt_avg = 5
# dt_avg = 10
# dt_avg = 50
# dt_avg = 100
# dt_avg = 250

# nt_batch = 20

path = 'T_click_1ms/l001g/' + str(dt) + 'ns'

data = {
    's2': {
        'T_avg': [],
        'n': [],
    },
    't0': {
        'T_avg': [],
        'n': [],
    }
}

# for w_0 in ['t0']:
for w_0 in ['t0', 's2']:
    # for w_0 in ['s2', 't0']:
    # ---------------------------------------------------------------------------------------------
    T_list = []

    for e in range(epoch):
        for e_s in range(epoch_size):
            # print(str(e * epoch_size + e_s) + '.pkl')
            T_ = pickle_load(path+'/' + w_0 + '/' +
                             str(e * epoch_size + e_s) + '.pkl')

            T_ = [round(i * 1e9) for i in T_]
            # print(T_)
            T_avg = np.sum(T_) / len(T_)

            # print()

            data[w_0]['T_avg'].append(T_avg)
    # print(len(T_))
    # M = log2(len(T_))
    # dt_avg = len(T_) / M
    T_avg_avg = np.sum(data[w_0]['T_avg']) / len(data[w_0]['T_avg'])
    # print(T_avg_avg)
    # data[w_0]['T_avg'] = [i - T_avg_avg for i in data[w_0]['T_avg']]

    # print(len(data[w_0]['T_avg']))
    # data[w_0]['T_avg'] = [i * 1e9 for i in data[w_0]['T_avg']]

    # print(data[w_0]['T_avg'])

    # exit(0)
    # T_ = pickle_load(path+'/'+w_0 + '_' + str(i) + '.pkl')
    # T_list += T_

    # print(len(T_list))
    # exit(0)
    # Assert(len(T_list) == NP * nt_batch, 'len(T_list) != np * 10')

    # T = T_list[-1]

    # T_str = None

    # T_str = time_unit(T)

    # if T >= 1e-3:
    #     T_list = [i * 1e3 for i in T_list]
    # elif T >= 1e-6:
    #     T_list = [i * 1e6 for i in T_list]
    # elif T >= 1e-9:
    #     T_list = [i * 1e9 for i in T_list]
    # T_list = [i * 1e9 for i in T_list]

    # print(T_list)

    # T_min = round(min(T_list))
    # T_max = round(max(T_list))
    # print(T_min, T_max)
    # ---------------------------------------------------------------------------------------------
    # T_list = np.round(T_list)
    # print(T_list)
    # ---------------------------------------------------------------------------------------------
    # print(int((T_max-T_min) / dt))
    # n = np.zeros(int((T_max) / dt + 1))
    # n = np.zeros(int((T_max-T_min) / dt + 1))

    # print('n:', n)

    # for t in T_list:
    #     # print(t, t/dt, int(t/dt)-int(T_min/dt))
    #     n[int(t / dt)] += 1
    #     # n[int(t / dt) - int(T_min/dt)] += 1
    #     # print(t)
    # print(n)
    # # exit(0)
    # Assert(np.sum(n) == NP * nt_batch, 'np.sum(n) == np * nt_batch')
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
    # if w_0 == 's2':
    #     data.append(go.Scatter(
    #         x=list(range(0, T_max+1, dt)),
    #         y=n,
    #         name='<b>|' + 's' + sub(2) + '〉'+'</b>',
    #     ))
    # elif w_0 == 't0':
    #     data.append(go.Scatter(
    #         x=list(range(0, T_max+1, dt)),
    #         y=n,
    #         name='<b>|' + 't' + sub(0) + '〉'+'</b>',
    #     ))
    # x = list(range(T_min, T_max+1, dt))

    # data.append(go.Scatter(
    #     x=list(range(T_min, T_max+1, dt)),
    #     y=gauss(x, sigma=1.0/sqrt(len(T_list)), x0=np.sum(x)/len(x)),
    #     name=w_0,
    # ))

# -------------------------------------------------------------
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from math import log2,ceil
np.random.seed(19680801)

# example data
mu = 2.244  # mean of distribution
sigma = sqrt(1.098)  # standard deviation of distribution
# x = mu + sigma * np.random.randn(437)
x = np.array(data[w_0]['T_avg']) / 1000
# print(x)
# exit(0)
size = (max(x)-min(x))
print(max(x)*1000, min(x)*1000)
num_bins = ceil(log2(len(x)))+1

fig, ax = plt.subplots()

weights = np.ones_like(x)/float(len(x))
# n, bins, patches=ax.hist(x, num_bins, weights=weights)
# the histogram of the data
n, bins, patches = ax.hist(x, num_bins, weights=weights, density=0, facecolor='g', alpha=0.75)
# print(n)
# print(bins)
# exit(0)
# add a 'best fit' line
x_ = np.linspace(0, 5, num_bins+1)
# y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
     # np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
     np.exp(-0.5 * (1 / sigma * (x_ - mu))**2))
# print(y)
# exit(0)
ax.plot(bins, y, '--')
ax.set_xlabel('Smarts')
ax.set_ylabel('Probability density')
ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

# Tweak spacing to prevent clipping of ylabel
fig.tight_layout()
plt.show()

exit(0)
# -------------------------------------------------------------
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, pi

E = 2.245
D = 1.0
mu, sigma = E, sqrt(D)
# # y = gauss(x, sigma, mu)
# print(mu, sigma)
# mu, sigma = 100, 15
y = mu + sigma * np.random.randn(10000)
# print(y)
# y = data[w_0]['T_avg']

# the histogram of the data
n, bins, patches = plt.hist(y, 100, density=True, facecolor='g', alpha=0.75)


plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
# plt.xlim(40, 160)
# plt.ylim(0, 0.03)
plt.grid(True)
plt.show()

exit(0)
# print(data)
# # exit(0)
# for w_0 in ['t0']:
dt_avg = round(dt_avg)
print(dt_avg)
# exit(0)
T_min = {}
T_max = {}
time = {}
t_click_avg = {}
d = {}

for w_0 in ['t0', 's2']:
    T_min[w_0] = round(min(data[w_0]['T_avg']))
    T_max[w_0] = round(max(data[w_0]['T_avg']))
    # print(T_min, T_max)
    data[w_0]['n'] = np.zeros(int((T_max[w_0]) / dt_avg + 1))

    for t in data[w_0]['T_avg']:
        data[w_0]['n'][int(t / dt_avg)] += 1

    data[w_0]['n'] /= np.sum(data[w_0]['n'])

    t_click_avg[w_0] = 0
    i = 0
    for t in list(range(0, int(T_max[w_0])+1, dt_avg)):
        t_click_avg[w_0] += t * data[w_0]['n'][i]
        i += 1

    i = 0
    d[w_0] = 0
    for t in list(range(0, int(T_max[w_0])+1, dt_avg)):
        d[w_0] += data[w_0]['n'][i] * (t - t_click_avg[w_0])**2
        i += 1
    
    # # print(data[w_0]['n'])
    # exit(0)
    if w_0 == 's2':
        plot_data.append(go.Scatter(
            x=list(range(0, int(T_max[w_0])+1, dt_avg)),
            y=data[w_0]['n'],
            name='<b>|' + 's' + sub(2) + '〉'+'</b>',
        ))
    elif w_0 == 't0':
        plot_data.append(go.Scatter(
            x=list(range(0, int(T_max[w_0])+1, dt_avg)),
            y=data[w_0]['n'],
            name='<b>|' + 't' + sub(0) + '〉'+'</b>',
        ))

# _x = list(range(0, int(T_max['t0'])+1, dt_avg))
# print(_x)
# print(gauss(_x, sqrt(2862), 2240))
# print(max(gauss(_x, sqrt(2862), 2240)))
# print(np.array(_x)-2245)
# print(gauss(_x, 1009, 2245))
# exit(0)

_x = list(range(0, int(T_max['t0'])+1, dt_avg))
plot_data.append(go.Scatter(
    x=_x,
    # y=gauss(_x, sqrt(100), t_click_avg['t0']),
    y=gauss(_x, sqrt(d['t0']), t_click_avg['t0']),
    name='<b>|' + 't' + sub(0) + '〉'+str(200)+'</b>',
))
# plot_data.append(go.Scatter(
#     x=_x,
#     # y=gauss(_x, sqrt(1000), t_click_avg['t0']),
#     y=gauss(_x, sqrt(d['t0']), t_click_avg['t0']),
#     name='<b>|' + 't' + sub(0) + '〉'+str(d['t0'])+'</b>',
# ))

_x = list(range(0, int(T_max['s2'])+1, dt_avg))
plot_data.append(go.Scatter(
    x=_x,
    y=gauss(_x, sqrt(d['s2']), t_click_avg['s2']),
    # y=gauss(_x, sqrt(100), t_click_avg['s2']),
    name='<b>|' + 's' + sub(2) + '〉'+str(sqrt(200))+'</b>',
))
# plot_data.append(go.Scatter(
#     x=_x,
#     y=gauss(_x, sqrt(d['s2']), t_click_avg['s2']),
#     # y=gauss(_x, sqrt(1000), t_click_avg['s2']),
#     name='<b>|' + 's' + sub(2) + '〉'+str(d['s2'])+'</b>',
# ))
print(t_click_avg)
print(d)

plot_builder = PlotBuilder2D({
    'to_file': False,
    'online': False,
    'data': plot_data,
    'x_title': 't, ns',
    # 'x_title': 'time, ' + str(T_str),

    # 'y_title': r'N',
    'y_title': r'p',

    # 'y_title': 'p' + sub('sink'),
    # 'y_title': 'dP/dt',

    'title': 'p(t),        T' + sub('click') + ' = ' + str(dt) + ' ns',
    # 'title': 'N(t),        T' + sub('click') + ' = ' + str(dt) + ' ns',

    # 'title': 'dP/dt',
    # 'title': w_0,
    'html': 'sink' + '.html',
    'as_annotation': True,
    # 'y_range': [0, 1700]
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
