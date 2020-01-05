import numpy as np

n = 100
p = [0.5] * n
# p = [1, 0.5, 0.25]
x = list(range(1, len(p)+1))

q = 1

P = []

for i in range(len(x)):
    P.append(p[i] * q)
    q *= 1 - p[i]

print(P)
print(p)
print(x)


def M(p, t):
    m = 0

    for i in range(len(p)):
        m += p[i] * t[i]

    return m, m / np.sum(p)


print(M(P, x))
