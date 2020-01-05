import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, pi

dt = 500
states = {
    't0': {
        'N': 1000,
        'x': [],
        'y': [],
        'x0': 5957.7974/1000.0,
    },
    's2': {
        'N': 1000,
        'x': [],
        'y': [],
        'x0': 5172.5059/1000.0,
    }
}
x1 = 0
x2 = 6.5

# x1 = 2.5
# x1 = 20
# x2 = 21.5
# x2 = 4.5
dx = 0.01

def gauss(x, sigma, x0):
    x = np.array(x)

    return 1.0/(sigma*sqrt(2*pi)) * np.exp((-(x-x0)**2) / (2*sigma**2))

# import numpy as np
# import matplotlib.pyplot as plt

# Fixing random state for reproducibility
# np.random.seed(19680801)
x = np.arange(x1, x2+dx, dx)
mu, sigma = 2.245, sqrt(1.000)
y = gauss(x, sigma, mu)

# mu, sigma = 100, 15
y = mu + sigma * np.random.randn(10000)
print(y)
exit(0)

# the histogram of the data
n, bins, patches = plt.hist(y, 500, density=False, facecolor='g', alpha=0.75)


plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
# plt.xlim(40, 160)
# plt.ylim(0, 0.03)
plt.grid(True)
plt.show()
# Copy to clipboard


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