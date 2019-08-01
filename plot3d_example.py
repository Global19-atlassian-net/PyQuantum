from PyQuantum.Tools.PlotBuilder3D import *
from PyQuantum.Tools.CSV import *

# ---------------------------------------------------------------------------------------------------------------------
x_data = [5, 6, 7]
y_data = [8, 9]
z_data = [
    [10, 20, 30],
    [40, 50, 60],
]
# ---------------------------------------------------------------------------------------------------------------------

# print(x_data)
# print(y_data)
# print(z_data)

# exit(0)
# y_data = [1, 2, 3]
# z_data = [
#     [1, 2, 3],
#     [1, 2, 3],
#     [1, 2, 3],
# ]

plot_builder = PlotBuilderData3D({
    'title': 'sink',

    'width': 1100,
    'height': 800,

    'to_file': False,
    'online': False,
    # 'data': data,
    'x_title': 'l/w<sub>c</sub>',
    'y_title': 'g/w<sub>c</sub>',
    'z_title': 'time',

    'x_data': x_data,
    'y_data': y_data,
    'z_data': z_data,
    # 'y_title': 'dP/dt',
    # 'title': 'dP/dt',
    # 'title': w_0,
    'html': '3d.html',
    'x_range': [min(x_data), max(x_data)],
    'y_range': [min(y_data), max(y_data)],
    # 'z_range': [min(z_data), max(z_data)],

    'y_scale': 1,

    'ticks': {
        'title': {
            'size': 20,
        },
        'family': 'Lato',
        'color': '#222',
        'size': 14,
    },
})

plot_builder.make_plot()
