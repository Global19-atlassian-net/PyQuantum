from PyQuantum.Common.Assert import *
import sys


def Print(self, mode='sparse', precision=0):
    if mode == 'full':
        for i in range(self.m):
            self.print_row(i)
            print()
    elif mode == 'non-zero':
        for k, v in self.row.items():
            if v['count'] != 0:
                self.print_row(k, precision)
                print()
    elif mode == 'sparse':
        for k, v in self.ind.items():
            for k_ind, j_ind in enumerate(v):
                print('(', k, ', ', j_ind, ') ',
                      self.items[k][k_ind], sep='')

    return


def print_rows(self, rows=None):
    if rows is None:
        for i in self.row:
            print(i)
    else:
        for i in rows:
            print(i)


def print_row(self, i, sep='\t', precision=0, file=sys.stdout):
    Assert(i >= 0, "i < 0", cf())

    if i in self.row:
        row = []

        for j in range(self.n):
            found = False

            for k, ind_j in enumerate(self.row[i]['ind']):
                # print(self.row[i]['ind'], 'ind_j=', ind_j, 'j=', j)
                if ind_j == j:
                    row += [self.row[i]['items'][k]]
                    found = True
                    break

            if not found:
                row += [0]
                # re = format(value.real, "." + str(precision) + "f")
        # v =
        row_str = sep.join(
            [str(format(i, "." + str(precision) + "f")) for i in row])
    else:
        row_str = sep.join(['0' for i in range(self.n)])

    print(row_str, end='', file=file)


def to_csv(self, filename):
    with open(filename, 'w') as file:
        for i in range(self.m):
            self.print_row(i, sep=',', file=file)
            print(file=file)
