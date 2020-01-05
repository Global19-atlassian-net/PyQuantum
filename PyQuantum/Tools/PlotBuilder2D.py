import plotly.plotly as py
# import chart_studio.plotly as py
# import chart_studio
import plotly.graph_objs as go
# import chart_studio.plotly.graph_objs as go

# from PyQuantum.Tools.PlotBuilder2D import *

import plotly


# -------------------------------
def sup(s):
    if not isinstance(s, str):
        s = str(s)

    return '<sup>' + s + '</sup>'
# -------------------------------


# -------------------------------
def sub(s):
    if not isinstance(s, str):
        s = str(s)

    return '<sub>' + s + '</sub>'
# -------------------------------


token = [
    {
        'login': 'alexfmsu',
        'key': 'g8ocp0PgQCY1a2WqBpyr'
    },
    {
        'login': 'alexf-msu',
        'key': 'VSOCzkhAhdKQDuV7eiYq'
    },
    {
        'login': 'alexfmsu_anime1',
        'key': 'XvGFBp8VudOGfUBdUxGQ'
    },
    {
        'login': 'alexfmsu_distrib',
        'key': 'NmiOXaqFkIxx1Ie5BNju'
    },
    {
        'login': 'alexfmsu_movies',
        'key': '5kV1qs60mmivbVvXNJW6'
    }
]

token_num = 0


def change_token():
    global token_num
    token_num += 1

    if token_num >= len(token):
        print("LIMIT")
        exit(0)

    plotly.tools.set_credentials_file(
        token[token_num]['login'], token[token_num]['key'])


plotly.tools.set_credentials_file(token[0]['login'], token[0]['key'])
# chart_studio.tools.set_credentials_file(token[0]['login'], token[0]['key'])


class PlotBuilder2D:
    def __init__(self, args):
        self.title = args['title']

        self.x_title = args['x_title']
        self.y_title = args['y_title']

        self.data = args['data']

        self.html = args['html']

        self.to_file = args['to_file']if 'to_file' in args else None
        self.online = args['online'] if 'online' in args else None

        if 'as_annotation' in args:
            self.as_annotation = args['as_annotation']
            self.x_title_annotation = self.x_title
            self.y_title_annotation = self.y_title

            self.x_title = None
            self.y_title = None
        else:
            self.as_annotation = None

        self.x_min = min(self.data[0]['x'])
        self.x_max = max(self.data[0]['x'])

        self.y_min = min(self.data[0]['y'])
        self.y_max = max(self.data[0]['y'])

        for i in self.data[1:]:
            self.x_min = min(self.x_min, min(i['x']))
            self.x_max = max(self.x_max, max(i['x']))

            self.y_min = min(self.y_min, min(i['y']))
            self.y_max = max(self.y_max, max(i['y']))

        # print(self.x_title)
        # exit(0)

        # self.y_range = args['y_range'] if 'y_range' in args else [0, 1]

    def make_plot(self):
        layout = dict(
            annotations=[
                {
                    'xref': 'paper',
                    'yref': 'paper',
                    # 'x': -0.1,
                    # 'x': -0.095,
                    'x': -0.1175,
                    'xanchor': 'left',
                    'y': 0.5,
                    'yanchor': 'middle',
                    'text': self.y_title_annotation,
                    'showarrow': False,
                    'font': dict(
                        # --------------------------------
                        family='Lato',
                        # family="Courier New, monospace",
                        # family='Open Sans, sans-serif',
                        # --------------------------------

                        size=20,

                        color="#222"
                    ),
                }, {
                    'xref': 'paper',
                    'yref': 'paper',
                    # 'x': 0,
                    'x': 0.5,
                    'xanchor': 'center',
                    # 'y': -0.3,
                    'y': -0.175,
                    'yanchor': 'bottom',
                    'text': self.x_title_annotation,
                    'showarrow': False,
                    'font': dict(
                        # --------------------------------
                        family='Lato',
                        # family="Courier New, monospace",
                        # family='Open Sans, sans-serif',
                        # --------------------------------

                        size=20,

                        color="#222"
                    ),
                }],
            orientation=0,
            width=1024,
            height=600,
            titlefont=dict(
                # --------------------------------
                family='Lato',
                # family="Courier New, monospace",
                # family='Open Sans, sans-serif',
                # --------------------------------

                size=20,

                color="#222"
            ),
            title='<b>' + self.title + '</b>',
            xaxis={
                'title': self.x_title,
                'linewidth': 2,
                'ticks': 'outside',
                # 'zeroline': True,
                'showline': True,
                'zeroline': False,
                # 'showline': False,
                'titlefont': dict(
                    family='Lato',
                    #     color="#000000",
                    color="#222",
                    size=18,
                ),
                'tickfont': dict(
                    family='Lato',
                    #     color="#000000",
                    color="#222",
                    size=16,
                ),
                'range': [self.x_min, self.x_max],
            },
            yaxis={
                'title': self.y_title,
                # 'tickangle': 0,
                'range': [self.y_min, self.y_max],
                # 'autorange': True,
                'linewidth': 2,
                'ticks': 'outside',

                # 'zeroline': True,
                'showline': True,
                # 'ticks': 'outside',
                'zeroline': False,
                'titlefont': dict(
                    family='Lato',
                    #     color="#000000",
                    color="#222",
                    size=18,
                ),
                'tickfont': dict(
                    family='Lato',
                    #     color="#000000",
                    color="#222",
                    size=16,
                ),
                # 'tickangle': 90,
            },
            legend=go.layout.Legend(
                # x=0,
                # y=1,
                # traceorder="normal",
                font=dict(
                    # family="sans-serif",
                    size=16,
                    color="#222",
                    family='Lato',

                ),
                # bgcolor="LightSteelBlue",
                # bordercolor="Black",
                # borderwidth=2
            ),
        )

        fig = dict(data=self.data, layout=layout)

        # fig['layout'].update_layout(
        #     legend=go.layout.Legend(
        #         # x=0,
        #         # y=1,
        #         # traceorder="normal",
        #         font=dict(
        #             # family="sans-serif",
        #             size=22,
        #             # color="black"
        #         ),
        #         # bgcolor="LightSteelBlue",
        #         # bordercolor="Black",
        #         # borderwidth=2
        #     )
        # )

        if self.online:
            py.plot(fig, filename=self.html)
        # py.plot(fig, filename=filename)
        else:
            if self.to_file:
                done = False

                while not done:
                    try:
                        py.image.save_as(fig, filename=self.to_file)
                        done = True
                    except plotly.exceptions.PlotlyRequestError:
                        change_token()
                        break
            else:
                plotly.offline.plot(fig, filename=self.html)
            # plotly.offline.init_notebook_mode()
