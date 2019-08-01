import numpy as np

H0 = np.matrix([
    [5, 6, 7],
    [8, 9, 10],
    [11, 12, 13]
])

H1 = np.matrix([
    [1, 2],
    [3, 4]
])

H2 = np.matrix([
    [16],
])


size_1 = np.shape(H0)[0]
size_2 = np.shape(H1)[0]
size_3 = np.shape(H2)[0]

size = size_1+size_2+size_3

I = np.zeros([size, size])
I[0:size_1, 0:size_1] = H0

I[size_1:size_1+size_2, size_1:size_1+size_2] = H1

I[size_1+size_2:size, size_1+size_2:size] = H2

print(I)
# I = np.eye(size_1*size_2)

# I23 = np.zeros([size_2, size_2])
# # I23 = np.zeros([size_2+size_3, size_2+size_3])
# # I23 = np.zeros([size_2+size_3, size_2+size_3])
# I23[0, 0] = 1

# I12 = np.zeros([size_1+size_2, size_1+size_2])
# I12[size_1, size_1] = 1

# print(H0)
# print(I23)
# # I1 = np.cross(I23, H0)
# print(I1)

# # I2 = np.kron(I12, H1)

# # print(I2)
# # print(I)

# # print(np.kron(np.identity(3), m))
# # print(np.kron(m, np.identity(3)))
