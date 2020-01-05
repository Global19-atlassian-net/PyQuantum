import plotly.graph_objs as go
from math import sqrt, exp, pi
import numpy as np

from PyQuantum.Tools.PlotBuilder2D import *

# # 50
# dt = 50
# states = {
#     't0': {
#         'N': 1000,
#         'x': [],
#         'y': [],
#         'x0': 1551.2151/1000.0,
#     },
#     's2': {
#         'N': 1000,
#         'x': [],
#         'y': [],
#         'x0': 1125.5102/1000.0,
#     }
# }
# x1 = 0.5
# x2 = 2.0

# 100
# dt = 100
# states = {
#     't0': {
#         'N': 1000,
#         'x': [],
#         'y': [],
#         'x0': 2245.4666/1000.0,
#     },
#     's2': {
#         'N': 1000,
#         'x': [],
#         'y': [],
#         'x0': 1659.5631/1000.0,
#     }
# }
# x1 = 1.0
# x2 = 3.0

# # 250
# states = {
#     't0': {
#         'N': 1000,
#         'x': [],
#         'y': [],
#         'x0': 3791.6136/1000.0,
#     },
#     's2': {
#         'N': 1000,
#         'x': [],
#         'y': [],
#         'x0': 2980.4960/1000.0,
#     }
# }
# x1 = 2.5
# x2 = 4.5

# 50
dt = 100
states = {
    '0D': {
        'title':'<b>|0' + sub(1) +'〉' + '( |0' + sub(2) + '1' + sub(3) + '〉- |1'+sub(2)+'0'+sub(3)+'〉'+')</b>',
        'N': 1000,
        'x': [],
        'y': [],
        'x0': 16.596,
        'sigma': 237.767,
    },
    '000': {
        'title':'<b>|0' + sub(1) + '0' + sub(2) + '0' + sub(3) + '〉'+'</b>',
        'N': 1000,
        'x': [],
        'y': [],
        'x0': 22.243,
        'sigma': 360.992,
    },
    '0D0': {
        'title':'<b>|0' + sub(1) +'〉' + '( |0' + sub(2) + '1' + sub(3) + '〉- |1'+sub(2)+'0'+sub(3)+'〉'+')</b>',
        'N': 1000,
        'x': [],
        'y': [],
        'x0': 20.435,
        'sigma': 374.358,
    },
    '0D1': {
        'title':'<b>|0' + sub(2) +'〉' + '( |0' + sub(1) + '1' + sub(3) + '〉- |1'+sub(1)+'0'+sub(3)+'〉'+')</b>',
        'N': 1000,
        'x': [],
        'y': [],
        'x0': 20.435,
        'sigma': 374.358,
    },
    '0D2': {
        'title':'<b>|0' + sub(3) +'〉' + '( |0' + sub(1) + '1' + sub(2) + '〉- |1'+sub(1)+'0'+sub(2)+'〉'+')</b>',
        'N': 1000,
        'x': [],
        'y': [],
        'x0': 20.435,
        'sigma': 374.358,
    },
    # 't0': {
    #     'N': 1000,
    #     'x': [],
    #     'y': [],
    #     'x0': 5957.7974/1000.0,
    # },
    # 's2': {
    #     'N': 1000,
    #     'x': [],
    #     'y': [],
    #     'x0': 5172.5059/1000.0,
    # }
}

x1 = 10
x2 = 30

# x1 = 2.5
# x1 = 20
# x2 = 21.5
# x2 = 4.5
dx = 0.001

# print(np.arange(x1, x2+dx, dx))

for k in states.keys():
    # sigma = 1.0/sqrt(states[k]['N'])
    sigma = 1.0/sqrt(states[k]['sigma'])
    x0 = states[k]['x0']

    for x in np.arange(x1, x2+dx, dx):
        states[k]['x'].append(x)
        states[k]['y'].append(1.0/(sigma*sqrt(2*pi)) *
                              exp(-(x-x0)**2 / (2*sigma**2)))

    # print(states[k]['x'])
plt = PlotBuilder2D({
    # 'title': 'f(t),        T' + sub('click') + ' = ' + str(dt) + ' ns',
    'title': 'N(μ,σ'+sup('2')+'),        T' + sub('click') + ' = ' + str(dt) + ' ns',
    'x_title': 't, mks',
    'y_title': 'N(μ,σ'+sup('2')+')',
    'html': 'gauss.html',
    'to_file': False,
    'online': False,
    'data': [
    #     go.Scatter(
    #     # x=states['t0']['x'],
    #     # y=states['t0']['y'],
    #     name='<b>|' + 't' + sub(0) + '〉'+'</b>',
    # ),
        go.Scatter(
        x=states['0D']['x'],
        y=states['0D']['y'],
        name=states['0D']['title'],
    ),
        go.Scatter(
        x=states['000']['x'],
        y=states['000']['y'],
        name=states['000']['title'],
        # name='<b>|' + 's' + sub(2) + '〉'+'</b>',
    ),
        go.Scatter(
        x=states['0D0']['x'],
        y=states['0D0']['y'],
        name=states['0D0']['title'],
        # name='<b>|' + 's' + sub(2) + '〉'+'</b>',
    ),
        go.Scatter(
        x=states['0D1']['x'],
        y=states['0D1']['y'],
        name=states['0D1']['title'],
        # name='<b>|' + 's' + sub(2) + '〉'+'</b>',
    ),
        go.Scatter(
        x=states['0D2']['x'],
        y=states['0D2']['y'],
        name=states['0D2']['title'],
        # name='<b>|' + 's' + sub(2) + '〉'+'</b>',
    ),

    ],
    'as_annotation': True,

}
)

plt.make_plot()

# integrate(1.0/(1/sqrt(45)*sqrt(2*pi)) * exp(-(x)**2 / (2*(1/sqrt(45))**2))) dx from 64.62 to infinity
