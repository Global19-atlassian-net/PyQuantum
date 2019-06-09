from PyQuantum.Common.SparseMatrix.ItemHandler import remove, remove_by_jpos
from PyQuantum.Common.SparseMatrix.ItemHandler import check_zero
from PyQuantum.Common.Assert import *

# -----------------------------------------------------------


def add_row(self, i, k):
    Assert(i >= 0, 'i < 0', cf())
    Assert(i < self.m, 'i >= m', cf())

    if i not in self.row.keys():
        return

    if k == 0:
        return

    for j_pos, j in enumerate(self.row[i]['ind']):
        self.add_item(i, j_pos, k)


def sub_row(self, i, k):
    Assert(i >= 0, 'i < 0', cf())
    Assert(i < self.m, 'i >= m', cf())

    if i not in self.row.keys():
        return

    if k == 0:
        return

    for j_pos, j in enumerate(self.row[i]['ind']):
        self.sub_item(i, j_pos, k)


def mult_row(self, i, k):
    Assert(i >= 0, 'i < 0', cf())
    Assert(i < self.m, 'i >= m', cf())

    if i not in self.row.keys():
        return

    if k == 0:
        self.remove_row(i)
        return

    if k == 1:
        return

    if k == -1:
        for j_pos, j in enumerate(self.row[i]['ind']):
            self.row[i]['items'][j_pos] = -self.row[i]['items'][j_pos]
    else:
        for j_pos, j in enumerate(self.row[i]['ind']):
            self.mult_item(i, j_pos, k)

    return


def divide_row(self, i, k):
    Assert(k != 0, 'k == 0', cf())

    Assert(i >= 0, 'i < 0', cf())
    Assert(i < self.m, 'i >= m', cf())

    if i not in self.row.keys():
        return

    if k == 1:
        return

    if k == -1:
        for j_pos, j in enumerate(self.row[i]['ind']):
            self.row[i]['items'][j_pos] = -self.row[i]['items'][j_pos]
    else:
        for j_pos, j in enumerate(self.row[i]['ind']):
            self.div_item(i, j_pos, k)

    return


def remove_row(self, i):
    Assert(i >= 0, 'i < 0', cf())
    Assert(i < self.m, 'i >= m', cf())

    if i not in self.row.keys():
        return

    self.count -= self.row[i]['count']

    del self.row[i]


def swap_rows(self, i_1, i_2):
    Assert(i_1 >= 0, 'i < 0', cf())
    Assert(i_1 < self.m, 'i >= m', cf())

    Assert(i_2 >= 0, 'i < 0', cf())
    Assert(i_2 < self.m, 'i >= m', cf())

    if i_1 == i_2:
        return

    self.row[i_1], self.row[i_2] = self.row[i_2], self.row[i_1]
