from PyQuantum.Tools.PlotBuilder3D import *

plot_builder = PlotBuilder3D({
    'title': 'title',

    'x_title': 'x_title',
    'y_title': 'y_title',

    'width': 100,
    'height': 100,

    'online': True
})

plot_builder.prepare({
    'x_csv': 'Bipartite/out/10_5/x.csv',
    'y_csv': 'test_y.csv',
    'z_csv': 'test_z.csv',


})
