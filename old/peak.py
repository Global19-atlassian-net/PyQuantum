from matplotlib import pyplot as plt

import numpy as np
import pandas as pd
import math

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import peakutils

import os

min_n = 1
max_n = 50

thres_up = 0.5
thres_down = 0.8

plotly.tools.set_credentials_file(
    username="alexf-msu", api_key="VSOCzkhAhdKQDuV7eiYq")
# plotly.tools.set_credentials_file(username="alexfmsu", api_key="g8ocp0PgQCY1a2WqBpyr")


def get_period(fid_filename, make_plot=False):
    if not os.path.isfile(fid_filename):
        return None

    pd_data = pd.read_csv(fid_filename)
    # data = milk_data.iloc[:, 10]

    data = pd_data['fidelity'].tolist()

    # print((len(data)-1)/20000*1000)
    cb = np.array(data)
    # print(cb)
    cb_2 = 1 - cb

    HIGH = peakutils.indexes(cb, thres=thres_up / max(cb), min_dist=1)

    LOW = peakutils.indexes(
        cb_2, thres=thres_down / max(cb_2), min_dist=1)

    T = []

    for i in range(0, len(HIGH)-1):
        T.append(HIGH[i+1]-HIGH[i])

    print(T)

    if make_plot:
        trace = go.Scatter(
            x=[j for j in range(len(data))],
            y=data,
            mode='lines',
            name='Original Plot'
        )

        trace2 = go.Scatter(
            x=HIGH,
            y=[data[j] for j in HIGH],
            mode='markers',
            marker=dict(
                size=8,
                color='rgb(255,0,0)',
                # symbol='cross'
            ),
            name='Detected Peaks'
        )

        trace3 = go.Scatter(
            x=LOW,
            y=[data[j] for j in LOW],
            mode='markers',
            marker=dict(
                size=8,
                color='rgb(0,255,0)',
                symbol='cross'
            ),
            name='Detected Peaks'
        )

        data = [trace, trace2, trace3]

        plotly.offline.plot(data, filename=fid_filename+'.html')

    exit(1)
    # print(ind)
    # print(keys)
    return 1


def get_mean_peak(fid_filename, make_plot=False):
    if not os.path.isfile(fid_filename):
        return None

    pd_data = pd.read_csv(fid_filename)
    # data = milk_data.iloc[:, 10]

    data = pd_data['fidelity'].tolist()

    # print((len(data)-1)/20000*1000)
    cb = np.array(data)
    # print(cb)
    cb_2 = 1 - cb

    indices = peakutils.indexes(cb, thres=thres_up / max(cb), min_dist=1)

    indices_2 = peakutils.indexes(
        cb_2, thres=thres_down / max(cb_2), min_dist=1)
    # print(indices_2)
    ind = {}

    HIGH = []
    LOW = []

    for i in indices:
        ind[i] = 'max'
        HIGH.append(i)

    for i in indices_2:
        ind[i] = 'min'
        LOW.append(i)

    keys = sorted(ind.keys())

    PL_width = []
    PL_height = []
    PL_hw = []

    # print(LOW)
    # print(HIGH)
    # print(ind)
    # print(keys)

    for i in range(0, len(LOW) - 1):
        # print(LOW[i], LOW[i+1])

        MAX = 0
        MAX_H = data[LOW[i]]

        for m in keys:
            if(m > LOW[i] and m < LOW[i+1] and ind[m] == 'max'):
                if(data[m] > MAX_H):
                    # print("\t", m)
                    MAX = m
                    MAX_H = data[m]
                    # if(data[MAX])
                # MAX = max(m, MAX)
            if(m > LOW[i+1]):
                break

        if MAX > 0:
            w = abs(LOW[i] - LOW[i+1])/20000*1000
            # print("\t\t", LOW[i], LOW[i+1], data[LOW[i]], data[LOW[i+1]])
            h = MAX_H

            PL_width.append(w)
            PL_height.append(h)
            PL_hw.append(h/w)

            # print(MAX)

        #     # print(ind[LOW[i]])
        #     print(ind[m], end='')
        # print()
        # print(indices_2[i], indices_2[i+1])
        # for j in range(1, len(HIGH) - 1):

    # exit(1)
    # for i in range(1, len(keys) - 1):
    #     if ind[keys[i - 1]] == 'min' and ind[keys[i]] == 'max' and ind[keys[i + 1]] == 'min':
    #         w = abs(keys[i - 1] - keys[i + 1])
    #         h = data[keys[i]]

    #         PL_width.append(w)
    #         PL_height.append(h)
    #         PL_hw.append(h / w)

    # print(keys[i], w)

    # print(np.mean(PL_width))
    # print(PL_width)

    if make_plot:
        trace = go.Scatter(
            x=[j for j in range(len(data))],
            y=data,
            mode='lines',
            name='Original Plot'
        )

        trace2 = go.Scatter(
            x=indices,
            y=[data[j] for j in indices],
            mode='markers',
            marker=dict(
                size=8,
                color='rgb(255,0,0)',
                # symbol='cross'
            ),
            name='Detected Peaks'
        )

        trace3 = go.Scatter(
            x=indices_2,
            y=[data[j] for j in indices_2],
            mode='markers',
            marker=dict(
                size=8,
                color='rgb(0,255,0)',
                symbol='cross'
            ),
            name='Detected Peaks'
        )

        data = [trace, trace2, trace3]

        plotly.offline.plot(data, filename=fid_filename+'.html')

    return {'width': np.mean(PL_width), 'height': np.mean(PL_height), 'rel': 1/np.mean(PL_hw)}
    # return 1/np.mean(PL_hw)
    # return np.mean(PL_height)


WIDTH = []
HEIGHT = []
REL = []

for n in range(min_n, max_n):
    # make_plot = True
    make_plot = False
    # if n == 1 or n == 15:
    #     make_plot = True
    # else:
    #     make_plot = False

    data = get_mean_peak('Bipartite_n/out/' + str(n) +
                         '/z_0.csv', make_plot=make_plot)
    if data is None:
        break

    width = data['width']
    height = data['height']
    rel = data['rel']

    # print(n, width)
    WIDTH.append(width)
    HEIGHT.append(height)
    REL.append(rel)

print(WIDTH)

# plt.plot(np.linspace(1, len(WIDTH), len(WIDTH)), WIDTH, marker='o', linewidth=1)
# plt.show()
# from py import PYPLOT2D


def PYPLOT2D(data_0, online=True, filename="Plot", scale=1, to_file=''):
    data = []

    for i in data_0["y"]["data"]:
        plot = go.Scatter(
            x=data_0["x"]["data"],
            y=i,
            name="ph_1",

            line=dict(
                # color='blue',
                # color=("rgb(205, 12, 24)"),
                width=2
            ),
            mode='lines+markers',
            marker=dict(
                size=8,
                color='#036FE3',
                # color='rgb(0,0,0)',
                # color='blue',
                # symbol='cross'
            ),
        )

        data.append(plot)

    # print(data_0["x"])

    layout = dict(
        title=data_0["title"],
        width=1600,
        height=800*float(scale),
        # showgrid=False,
        margin=dict(l=150, t=-100, b=150),


        xaxis=dict(
            title=data_0["x"]["title"]+"<br>",
            titlefont=dict(
                color="#222",
                size=35,
            ),

            zeroline=True,

            rangemode='tozero',

            tickprefix=" "*50,
            ticks='outside',
            tickfont=dict(
                color="#000000",

                # color="#222",
                size=25,
            ),
            ticklen=10,

            linewidth=2,

            ticktext=data_0["x"]["ticktext"],
            # ticktext=data_0["x"]["ticktext"][::2],
            # tickvals=data_0["x"]["tickvals"][::2]
            tickvals=data_0["x"]["tickvals"]
        ),

        yaxis=dict(
            title=data_0["y"]["title"],
            titlefont=dict(
                color="#000000",
                # color="#222",
                size=35,
            ),

            zeroline=True,
            rangemode='tozero',

            ticks='outside',
            tickfont=dict(
                color="#000000",
                # color="#222",
                size=25,
            ),
            ticklen=10,
            tickprefix=" "*60,
            linewidth=2,
            # tickcolor='black',

            # tickvals=np.around(np.linspace(0, 25, 6), 1),
            # ticktext=np.around(np.linspace(0, 1, 11), 1),
            # ticktext=np.linspace(0, 1, 11),
            # tickvals=data_0["y"]["tickvals"],
            # ticktext=data_0["y"]["ticktext"],

            # tickvals=np.around(np.linspace(0, 1, 6), 1),
            # range=[0, 1],

            tickvals=data_0["y"]['tickvals'],
            # tickvals=np.around(np.linspace(0, 30, 6), 1),
            range=data_0["y"]['range'],
        ),
    )

    fig = dict(data=data, layout=layout,

               )

    if online:
        py.plot(fig, filename=filename)
    else:
        if to_file:
            done = False

            while not done:
                try:
                    py.image.save_as(fig, filename=to_file)
                    done = True
                except plotly.exceptions.PlotlyRequestError:
                    change_token()

            return
        # plotly.offline.init_notebook_mode()
        plotly.offline.plot(fig, filename=filename + ".html")


# print(np.around(np.linspace(0, WIDTH[-1], 1), 3))

p = np.around(np.linspace(1, len(WIDTH) + 1, len(WIDTH) + 1), 3)
print(np.around(np.linspace(0, np.max(WIDTH), 11), 3))
# print(np.linspace(0, 600, 10))
# print(np.linspace(1, len(WIDTH) + 1, len(WIDTH) + 1)
# print([1] + list(np.arange(5, len(WIDTH), 5)))
# print(int(WIDTH[-1])+1, 5)))
print([1] + list(np.arange(5, len(WIDTH)+2, 5)))
PYPLOT2D(
    data_0={
        "title": '',
        # "title": "<b>w<sub>c</sub> = w<sub>a</sub> = 2 PI x 0.5 MHz;\tg / (hw<sub>c</sub>) = 0.001<br>" +
        # "m = g<b>",
        "x": {
            "title": "n",
            # "title": "Time, " + T_str_mark(config.T),
            # "data": PL_width,
            "data": np.linspace(1, len(WIDTH)+1, len(WIDTH)),
            "ticktext": [1] + list(np.arange(5, len(WIDTH)+2, 5)),
            "tickvals": [1] + list(np.arange(5, len(WIDTH)+2, 5))
            # "tickvals": PL_width
        },
        "y":
        {
            # "title": "Avg. peak height",
            # "title": "Avg. peak width, ns",
            # "title": "⟨height⟩",
            "title": "⟨width⟩, ns",
            # "title": "⟨width / height⟩",
            # "title": "Avg. peak height/width",
            # "tickvals": np.linspace(0, 600, 10),
            "tickvals": np.around(np.linspace(0, 30, 6), 1),
            "ticktext": "",
            # "tickvals": np.around(np.linspace(0, WIDTH[-1], 50), 1),
            # "ticktext": np.around(np.linspace(0, WIDTH[-1], 50), 1),
            "data":
            [
                WIDTH,
            ],
            'range': [0, 30],
        },
    },

    online=False,
    # filename=config.path + "/" + "Fidelity"
    filename="Width"
)

PYPLOT2D(
    data_0={
        "title": '',
        # "title": "<b>w<sub>c</sub> = w<sub>a</sub> = 2 PI x 0.5 MHz;\tg / (hw<sub>c</sub>) = 0.001<br>" +
        # "m = g<b>",
        "x": {
            "title": "n",
            "data": np.linspace(1, len(HEIGHT)+1, len(HEIGHT)),
            "ticktext": [1] + list(np.arange(5, len(WIDTH)+2, 5)),
            "tickvals": [1] + list(np.arange(5, len(WIDTH)+2, 5)),
        },
        "y":
        {
            "title": "⟨height⟩",
            # "tickvals": np.linspace(0, 600, 10),
            "tickvals": np.around(np.linspace(0, 1, 6), 3),
            "ticktext": "",
            # "tickvals": np.around(np.linspace(0, WIDTH[-1], 50), 1),
            # "ticktext": np.around(np.linspace(0, WIDTH[-1], 50), 1),
            "data":
            [
                HEIGHT,
            ],
            'range': [0, 1],
            # 'range': [0, math.ceil(np.max(HEIGHT))],
        },
    },

    online=False,
    # filename=config.path + "/" + "Fidelity"
    filename="Height"
)

PYPLOT2D(
    data_0={
        "title": '',
        # "title": "<b>w<sub>c</sub> = w<sub>a</sub> = 2 PI x 0.5 MHz;\tg / (hw<sub>c</sub>) = 0.001<br>" +
        # "m = g<b>",
        "x": {
            "title": "n",

            # "title": "Time, " + T_str_mark(config.T),
            # "data": PL_width,
            "data": np.linspace(1, len(REL)+1, len(REL)),
            "ticktext": [1] + list(np.arange(5, len(WIDTH)+2, 5)),
            "tickvals": [1] + list(np.arange(5, len(WIDTH)+2, 5)),
            # "tickvals": PL_width
        },
        "y":
        {
            "title": "⟨width / height⟩, ns",

            "ticktext": "",
            "tickvals": np.around(np.linspace(0, 30, 6), 1),
            # "ticktext": np.around(np.linspace(0, WIDTH[-1], 50), 1),
            "data":
            [
                REL,
            ],
            'range': [0, 30],
        },
    },

    online=False,
    # filename=config.path + "/" + "Fidelity"
    filename="Rel"
)
