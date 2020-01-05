# -------------------------------------------------------------------------------------------------
# scientific
import numpy as np
# -------------------------------------------------------------------------------------------------
# system
from copy import copy
# -------------------------------------------------------------------------------------------------
# PyQuantum.Tools
from PyQuantum.Tools.Distributions import Expectation, GeometricDistribution
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


# -------------------------------------------------------------------------------------------------
n_dots = 500

dt = 10

n_trials = 100

print('-'*100)
print('n_dots:', n_dots)
print('dt:', dt)
print('n_trials:', n_trials)
print('-'*100)
print()
# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------
p_sink = np.abs(np.random.random_sample(n_dots))

p_sink = sorted(p_sink)

T = list(range(1, len(p_sink)+1))
T_dt = T[dt-1::dt]
# T_dt = list(range(dt, len(T), dt))
p_sink_dt = p_sink[dt-1::dt]

data = Sink(P=p_sink, T=T)

if __debug__:
    data.print()
# -------------------------------------------------------------------------------------------------

# BEGIN----------------------------------------- EXPERIMENT ---------------------------------------
T_click = []

max_t = n_dots

if __debug__:
    print('-'*50)

click = []

for _ in range(n_trials):
    T_click_trial = []

    click_trial = {
        'T': [],
        'step': [],
    }

    t_ = T_dt[0]
    t_step = 1

    while t_ < max_t:
        coin = np.random.random_sample(1)[0]

        if __debug__:
            print('(', t_step, ', ', t_, ')', sep='')
            print('p_sink_dt =', p_sink_dt[t_step])
        # print('t_ =', t_)
        # print('t_step =', t_step)

        if coin <= p_sink_dt[t_step]:
            T_click_trial.append(T_dt[t_step] / dt)
            click_trial['T'].append(T_dt[t_step] / dt)
            click_trial['step'].append(t_step)

            if __debug__:
                cprint(str(coin) + ' <= ' +
                       str(p_sink_dt[t_step]), color='green', attrs=['bold'])
            t_step = 0
        else:
            if __debug__:
                cprint(str(coin) + ' > ' +
                       str(p_sink_dt[t_step]), color='red', attrs=['bold'])

        t_step += 1
        t_ += dt

        if __debug__:
            print('-'*50)

    T_click.append(T_click_trial)
    click.append(click_trial)

T_clicks_total = []

N_clicks_total = 0

# print(click)
# exit(0)
for i in click:
    print(i['step'])
    N_clicks_total += len(i['step'])

    for step in i['step']:
        T_clicks_total.append(step * dt)

N_click_avg = np.sum([len(i['step']) for i in click]) / len(T_click)
# END------------------------------------------- EXPERIMENT ---------------------------------------

data_dt = Sink(p_sink_dt, T_dt)

if __debug__:
    data_dt.print()

# -------------------------------------------------------------------------------------------------
p_, t_ = GeometricDistribution(data_dt.data['P'], T)
data_theor = Sink(p_, t_)


E, E_normed = Expectation(data_theor.data['P'], data_theor.data['T'])
# -------------------------------------------------------------------------------------------------

# =================================================================================================
cprint('EXPERIMENT:', color='yellow', attrs=['bold'])

print("N_clicks_total:", N_clicks_total)
print("T_click_total_sum:", np.sum(T_clicks_total))
T_click_avg = np.sum(T_clicks_total) / N_clicks_total
print("T_click_avg:", T_click_avg)
print('\tN_click_avg_avg: ', N_click_avg, sep='')
print('\tT_click_avg_avg: ', n_dots / N_click_avg, sep='')
print('\tT_click_steps_avg: ', n_dots / dt / N_click_avg, sep='')

cprint('THEORY:', color='yellow', attrs=['bold'])

print('T_click_avg: ', E * dt)
# print('theor: ', P_M, ', ', (n_dots) / T_M, sep='')
# print('theor: ', P_M, ', ', len(T_dt), sep='')
# =================================================================================================
# print("abs_err:", abs(P_M * dt - T_click_avg))
# =================================================================================================
