from PyQuantum.Tools.CSV import *
import plotly.graph_objs as go
import numpy as np
from PyQuantum.Tools.PlotBuilder2D import *

# data = []

# data.append(go.Scatter(
#     x=[1, 2, 3],
#     y=[4, 5, 6],
#     name="w_0['title']",
# ))

# plot_builder = PlotBuilder2D({
#     'title': 'M[p<sub>sink</sub>]<sub>|t<sub>0</sub>〉</sub> - M[p<sub>sink</sub>]<sub>|s<sub>2</sub>〉</sub>',
#     # 'title': '(M[p<sub>sink</sub>]<sub>|t<sub>0</sub>〉</sub> - M[p<sub>sink</sub>]<sub>|s<sub>2</sub>〉</sub>) (t)',

#     'x_title': 'l/g',
#     'y_title': 'ΔM, ',

#     'data': data,

#     'to_file': False,

#     'html': 'M' + '.html',
#     'online': False,
# })

# plot_builder.make_plot()


# exit(0)
# def df2(x, y):
#     f_xn = y[-1]
#     xn = x[-1]

#     DF = []
#     t = []

#     for i in range(1, len(y)-1):
#         df_ = (y[i+1]-y[i-1]) / (x[i+1] - x[i-1])
#         DF.append(df_)
#         t.append(x[i])

#     return DF, t


data = []

M_str = ''

M_list = {
    's_2': [],
    't_0': []
}

for w_0 in [
    {
        'name': 's_2',
        'title': '|s<sub>2</sub>〉',
    },
    {
        'name': 't_0',
        'title': '|t<sub>0</sub>〉',
    }
]:
    gamma = []

    # M_list = []

    for coeff in list(np.arange(0.01, 1.01, 0.01)) + list(np.arange(10.0, 210.0, 10.0)):
        # for coeff in np.arange(10.0, 210.0, 10.0):
        # for coeff in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0]:
        # for coeff in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 100.0, 110.0, 120.0, 130.0, 140.0, 150.0, 160.0]:
        # for coeff in [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]:
        # for coeff in np.arange(0.01, 1.01, 0.01):
        coeff = np.round(coeff, 3)

        T_list = list_from_csv('MM/M_' + str(coeff) + '/T_' + w_0['name'] + '.csv')
        T_list = np.array(T_list)

        sink_list = list_from_csv('MM/M_' + str(coeff) + '/sink_' + w_0['name'] + '.csv')
        sink_list = np.array(sink_list)

        sink_list /= np.sum(sink_list)

        M = 0

        for i in range(len(T_list)):
            M += sink_list[i] * T_list[i]

        M_list[w_0['name']].append(M)

        gamma.append(coeff)


M_diff = []

# print(M_list['s_2'])
# print(M_list['t_0'])

for j in range(len(M_list['s_2'])):
    M_diff.append(M_list['t_0'][j] - M_list['s_2'][j])
    # M_list = np.array(M_list)
# print(M_diff)

M_diff = np.array(M_diff)

if max(M_diff) > 1e6:
    M_diff *= 1e-6
    M_str = '10<sup>6</sup>'
elif max(M_diff) > 1e3:
    M_diff *= 1e-3
    M_str = '10<sup>3</sup>'
elif max(M_diff) > 1e-3:
    M_diff *= 1e3
    # M_str = '10<sup>-3</sup>'
    M_str = 'ms'
elif max(M_diff) > 1e-6:
    M_diff *= 1e6
    # M_str = '10<sup>-6</sup>'
    M_str = 'mks'
elif max(M_diff) > 1e-9:
    M_diff *= 1e9
    M_str = 'ns'
    # M_str = '10<sup>-9</sup>'

data.append(go.Scatter(
    x=gamma,
    y=M_diff,
    name=w_0['title'],
))

plot_builder = PlotBuilder2D({
    'title': 'M[p<sub>sink</sub>]<sub>|t<sub>0</sub>〉</sub> - M[p<sub>sink</sub>]<sub>|s<sub>2</sub>〉</sub>',
    # 'title': '(M[p<sub>sink</sub>]<sub>|t<sub>0</sub>〉</sub> - M[p<sub>sink</sub>]<sub>|s<sub>2</sub>〉</sub>) (t)',

    'x_title': 'l/g',
    'y_title': 'ΔM, ' + M_str,

    'data': data,

    'to_file': False,

    'html': 'M' + '.html',
    'online': False,
})

plot_builder.make_plot()
