# -------------------------------------------------------------------------------------------------
# scientific
from PyQuantum.Tools.PlotBuilder2D import *
from math import sqrt, exp, pi
import plotly.graph_objs as go
import numpy as np
# -------------------------------------------------------------------------------------------------
# system
from copy import copy
# -------------------------------------------------------------------------------------------------
# PyQuantum.Tools
from PyQuantum.Tools.Distributions import Expectation, GeometricDistribution, Variance
from PyQuantum.Tools.Pickle import *
from PyQuantum.Tools.Print import *
from PyQuantum.Tools.Units import *
# -------------------------------------------------------------------------------------------------


# =================================================================================================
class Sink:
    def __init__(self, P=[], T=[]):
        self.data = {
            'P': copy(P),
            'T': copy(T),
        }

    def set_P(self, P):
        self.data['P'] = copy(P)

    def set_T(self, T):
        self.data['T'] = copy(T)

    def print(self):
        for i in range(len(self.data['P'])):
            print("{:3f}".format(self.data['T'][i]),
                  ': ', self.data['P'][i], sep='')

        print()
# =================================================================================================


# w_0 = 't_11_000'

# w_0 = '10_000'
w_0 = '10_D'

# w_0 = '10_0D'
# w_0 = '10_1D'
# w_0 = '10_2D'

# w_0 = 't0'
# path = 'sink3/1ms_l001g'
# path = 'sink/1ms_l001g'
path = 'sink3/0_1ms_01ns_l10g_l10g'

T_list = pickle_load(path+'/T_list_' + w_0 + '.pkl')
T_list = pickle_load(path+'/T_list_' + w_0 + '.pkl')
T = T_list[1:]

# p_sink_list = pickle_load(path+'/sink_list_' + w_0 + '_12.pkl')
p_sink_list = pickle_load(path+'/sink_list_' + w_0 + '.pkl')
p_sink = p_sink_list[1:]

data = Sink(P=p_sink, T=T)
# print(len(p_sink_list))
# print(p_sink_list[1])
# print(time_unit_full(T_list[1]))
# exit(0)
# -------------------------------------------------------------------------------------------------
dt = 100
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
T_dt = T[dt-1::dt]

p_sink_dt = p_sink[dt-1::dt]

data_dt = Sink(p_sink_dt, T_dt)
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
p_, t_ = GeometricDistribution(data_dt.data['P'], T)
data_theor = Sink(p_, t_)


E, E_normed = Expectation(data_theor.data['P'], data_theor.data['T'])
D = Variance(data_theor.data['P'], data_theor.data['T'], E)

print(data_theor.data['T'])
print('E = ', E)
print('E = ', E*dt*1e6)
print('D = ', D*dt*1e6)
print('sigma = ', sqrt(D))
print('sigma = ', time_unit_full(sqrt(D) * dt))
# exit(0)
# -------------------------------------------------------------------------------------------------

# =================================================================================================
cprint('THEORY:', color='yellow', attrs=['bold'])

print('T_click_avg: ', time_unit_full(E * dt))
# =================================================================================================
# print("abs_err:", abs(P_M * dt - T_click_avg))
# =================================================================================================
# print(E*dt*1e6)
# exit(0)
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, pi

# dt = 500
# states = {
#     't0': {
#         'N': 1000,
#         'x': [],
#         'y': [],
#         'x0': 5957.7974/1000.0,
#     },
#     's2': {
#         'N': 1000,
#         'x': [],
#         'y': [],
#         'x0': 5172.5059/1000.0,
#     }
# }
# x1 = 0
# x2 = 6.5

# # x1 = 2.5
# # x1 = 20
# # x2 = 21.5
# # x2 = 4.5
# dx = 0.01

def gauss(x, sigma, x0):
    x = np.array(x)

    return 1.0/(sigma*sqrt(2*pi)) * np.exp((-(x-x0)**2) / (2*sigma**2))

# import numpy as np
# import matplotlib.pyplot as plt

# Fixing random state for reproducibility
# np.random.seed(19680801)
# x = np.arange(x1, x2+dx, dx)
D *= 1000
mu, sigma = E*1e6*dt, sqrt(D)*1e6*dt
# y = gauss(x, sigma, mu)
print(mu, sigma)
print(mu*1e3, sigma*1e3)
exit(0)
# mu, sigma = 100, 15
# y = mu + sigma * np.random.randn(10000)
# print(y)

# the histogram of the data
# n, bins, patches = plt.hist(y, 500, density=True, facecolor='g', alpha=0.75)


# plt.xlabel('Smarts')
# plt.ylabel('Probability')
# plt.title('Histogram of IQ')
# plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
# # plt.xlim(40, 160)
# # plt.ylim(0, 0.03)
# plt.grid(True)
# plt.show()
# Copy to clipboard

import numpy as np
import matplotlib.pyplot as plt

x1 = 0
x2 = 30
dx = 1e-3
x = np.arange(x1, x2+dx, dx) 
sigma*=1e3
mu*=1e3
print(sigma, mu)
age = gauss(x, sigma, mu)
# age = np.random.normal(loc=1, size=1000) # a normal distribution
# salaray = np.random.normal(loc=-1, size=10000) # a normal distribution
print(age)


_, bins, _ = plt.hist(age, bins=1000, range=[x1, x2], density=True)
# _ = plt.hist(salaray, bins=bins, alpha=0.5, density=True)
plt.show()



exit(0)

# N_points = 100000
# n_bins = 20

# # Generate a normal distribution, center at x=0 and y=5
# x = np.random.randn(N_points)
# y = .4 * x + np.random.randn(100000) + 5

# fig, axs = plt.plot(1, sharey=True, tight_layout=True)

# # We can set the number of bins with the `bins` kwarg
# axs[0].hist(x, bins=n_bins)
# # axs[1].hist(y, bins=n_bins)

# plt.show()

# import matplotlib.pyplot as plt
# import numpy as np

# def histogram(data, n_bins, cumulative=False, x_label = "", y_label = "", title = ""):
#     _, ax = plt.subplots()
#     ax.hist(data, n_bins = n_bins, cumulative = cumulative, color = '#539caf')
#     ax.set_ylabel(y_label)
#     ax.set_xlabel(x_label)
#     ax.set_title(title)

# histogram([1,2,3], n_bins=2)
# ==============

states = {
    't0': {
        'N': 1000,
        'x': [],
        'y': [],
        'x0': 2.245,
    },
    # 's2': {
    #     'N': 1000,
    #     'x': [],
    #     'y': [],
    #     'x0': 5172.5059/1000.0,
    # }
}
x1 = 0
x2 = 4

# x1 = 2.5
# x1 = 20
# x2 = 21.5
# x2 = 4.5
dx = 0.0001
# sigma = sqrt(D)
# print(time_unit_full( * dt))
# print(D*1e12)
# print(time_unit_full(sqrt(D)*dt))
# exit(0)
sigma = sqrt(1000)
for k in states.keys():
    # sigma = 1.097
    # sigma = 1.0/sqrt(states[k]['N'])
    x0 = states[k]['x0']

    for x in np.arange(x1, x2+dx, dx):
        states[k]['x'].append(x)
        states[k]['y'].append(1.0/(sigma*sqrt(2*pi)) *
                              exp(-(x-x0)**2 / (2*sigma**2)))

plt = PlotBuilder2D({
    # 'title': 'f(t),        T' + sub('click') + ' = ' + str(dt) + ' ns',
    'title': 'N(μ,σ'+sup('2')+'),        T' + sub('click') + ' = ' + str(dt) + ' ns',
    'x_title': 't, mks',
    'y_title': 'N(μ,σ'+sup('2')+')',
    'html': 'gauss.html',
    'to_file': False,
    'online': False,
    'data': [
        go.Scatter(
            x=states['t0']['x'],
            y=states['t0']['y'],
            name='<b>|' + 't' + sub(0) + '〉'+'</b>',
        ),
        # go.Scatter(
        #     x=states['s2']['x'],
        #     y=states['s2']['y'],
        #     name='<b>|' + 's' + sub(2) + '〉'+'</b>',
        # ),
    ],
    'as_annotation': True,

}
)

plt.make_plot()
