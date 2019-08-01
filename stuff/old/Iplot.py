# # from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# from plotly.offline import init_notebook_mode, iplot

# # print __version__ # requires version >= 1.9.0

# # plot([go.Scatter(x=[1, 2, 3], y=[3, 1, 6])])
# # init_notebook_mode(connected=True)
# iplot([{"x": [1, 2, 3], "y": [3, 1, 6]}])


# import plotly.plotly as py
# import plotly.graph_objs as go

# trace0 = go.Scatter(
#     x=[1, 2, 3, 4],
#     y=[10, 15, 13, 17]
# )
# trace1 = go.Scatter(
#     x=[1, 2, 3, 4],
#     y=[16, 5, 11, 9]
# )
# data = [trace0, trace1]

# py.iplot(data, filename='basic-line', auto_open=True)


from PyQuantum.Common.Quantum.Operators import Hadamard, sigma_x, sigma_y, sigma_z

print(sigma_x())
print(sigma_y()[0, 1])

print(sigma_y())
print(sigma_z())
print(Hadamard())
