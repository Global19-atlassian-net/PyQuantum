from PyQuantum.Tools.PlotBuilder3D import *
from PyQuantum.Tools.CSV import *

# ---------------------------------------------------------------------------------------------------------------------
g_list = np.arange(0.01, 1.01, 0.01) * 1e-2
l_list = list(np.arange(4.0, 5.1, 0.1))
# l_list = list(np.arange(0.01, 1.01, 0.01))

path = '/media/alexfmsu/023ae322-693f-4e87-8606-08ab8c27190a/sink_out'
l_threshold = 0.9
max_l = 10
state = 't_0'

g_list = np.round(g_list, 4)
l_list = np.round(l_list, 2)

p = []

for g in g_list:
    p_g = []

    for l in l_list:
        t = list_from_csv(path + '/' + str(l_threshold) + '_' + str(max_l) + '/' + str(l_threshold) + '/' + state +
                          # t = list_from_csv(path + '/' + str(l_threshold) + '/' + 't_0' +
                          '/' + 't_' + str(g) + '_' + str(l) + '.csv')[0][0]
        # t = list_from_csv('t_0/t_' + str(g) + '_' + str(l) + '.csv')[0][0]

        p_g.append(float(t))

    p_g = np.array(p_g) * 1e6

    p.append(p_g)

# print(len(t_0), len(t_0[0]))
# for i in t_0:
#     print(i)

# exit(0)

x_data = l_list
y_data = g_list
z_data = p
# ---------------------------------------------------------------------------------------------------------------------

# exit(0)
# x_data = list_from_csv('sink_l_g/t_0/g.csv')
# x_data = [float(i) for i in x_data[0]]

# y_data = list_from_csv('sink_l_g/t_0/l.csv')
# y_data = [float(i) for i in y_data[0]]

# z_data = list_from_csv('sink_l_g/t_0/t.csv')
# z_data = [[float(i) * 1e3 for i in j] for j in z_data]


# ---------------------------------------------------------------------------------------------------------------------
# x_data = [5, 6, 7]
# y_data = [8, 9]
# z_data = [
#     [10, 20, 30],
#     [40, 50, 60],
# ]
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
    'x_title': 'l',
    'y_title': 'g',
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
            'size': 30,
        },
        'family': 'Lato',
        'color': '#222',
        'size': 16,
    },
})

plot_builder.make_plot()
