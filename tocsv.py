import csv
import pandas as pd

# df = pd.DataFrame([
#     [5, 6, 7],
#     [50, 60, 70],
# ], columns=None)
df = pd.DataFrame([[5, 6, 7]], columns=None)

df.to_csv('1.csv', index=None, header=False)


d = pd.read_csv('1.csv')

rows = []

with open('1.csv') as csvfile:
    csvreader = csv.reader(csvfile)
    # res = list(zip(*rows))
    # print(rows)
    for row in csvreader:
        rows.append(row)

print(rows)
# with open('1.csv', 'r') as f:
#     a = f.readline()
#     print(a)

# print(d)
# print(d.ndim)
# print(d.shape)
# print(d.loc[0, ])
