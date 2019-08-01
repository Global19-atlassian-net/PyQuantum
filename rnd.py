from PyQuantum.Tools.CSV import *
import numpy as np

lst = list_from_csv('rnd.csv')

lst = [float(i[0]) for i in lst]

for i in lst:
    print('%s' % (repr(round(i, 10))))
# print(i)
# print(np.round(i, 3))
