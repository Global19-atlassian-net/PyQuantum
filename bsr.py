import numpy as np
from scipy.sparse import lil_matrix

M = lil_matrix((3, 4), dtype=np.int8)
M.data[0,0] = 4

print(M.data)
print(M.toarray())