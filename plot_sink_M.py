from PyQuantum.Tools.CSV import *
from PyQuantum.Tools.Assert import *
import plotly.graph_objs as go
import numpy as np
from PyQuantum.Tools.PlotBuilder2D import *
from PyQuantum.Tools.Pickle import *


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

path = 'sink/1ms_l10g'

for w_0 in [
    {
        'name': 's2',
        'title': '|s<sub>2</sub>〉',
        # 'obj': s_2,
    },
    {
        'name': 't0',
        'title': '|t<sub>0</sub>〉',
        # 'obj': t_0,
    }
]:
    M_list = []

    T_list = pickle_load(path+'/T_list_' + w_0['name'] + '.pkl')
    # T_list = list_from_csv('MM/M_' + str(coeff) + '/T_' + w_0['name'] + '.csv')
    T_list = np.array(T_list, dtype=np.float64)

    sink_list = pickle_load(path+'/sink_list_' + w_0['name'] + '.pkl')
    # sink_list = list_from_csv('MM/M_' + str(coeff) + '/sink_' + w_0['name'] + '.csv')
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
    # gamma.append(coeff)

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
print(data)
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
