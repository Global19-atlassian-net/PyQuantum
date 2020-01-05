from PyQuantum.Tools.Pickle import *
import numpy as np

data = pickle_load('dt_s2_1ms.pkl')

print(data)

print(np.sum(data) / len(data) * 1e6)

print(len(data))
