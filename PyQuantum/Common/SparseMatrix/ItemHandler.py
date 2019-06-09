from PyQuantum.Common.Assert import *


# -----------------------------------------------
# input parameters are varified

def add_item(self, i, j_pos, value):
    self.row[i]['items'][j_pos] += value
    self.check_zero(i, None, j_pos)


def sub_item(self, i, j_pos, value, autoremove=True):
    # print('items:', self.row[i]['items'])
    # print(j_pos)
    self.row[i]['items'][j_pos] -= value

    if autoremove:
        self.check_zero(i, None, j_pos)


def mult_item(self, i, j_pos, value):
    self.row[i]['items'][j_pos] *= value
    self.check_zero(i, None, j_pos)


def div_item(self, i, j_pos, value):
    # print('v=', value)
    self.row[i]['items'][j_pos] /= value
    # print(j)
    self.check_zero(i, None, j_pos)
# -----------------------------------------------


def remove(self, i, j):
    for j_pos, ind_j in enumerate(self.row[i]['ind']):
        if ind_j == j:
            del self.row[i]['ind'][j_pos]
            del self.row[i]['items'][j_pos]

            self.row[i]['count'] -= 1

            if self.row[i]['count'] == 0:
                del self.row[i]

            self.count -= 1

            break


def remove_from_heap(self, i, j):
    found = False

    for v in self.heap:
        if v[0] == (i, j):
            self.heap.remove(v)
            found = True
            break

    Assert(found, 'not found', cf())


def remove_by_jpos(self, i, j_pos):
    del self.row[i]['ind'][j_pos]
    del self.row[i]['items'][j_pos]
    # print('\tdel:', self.row[i]['items'])
    self.row[i]['count'] -= 1

    if self.row[i]['count'] == 0:
        del self.row[i]

    self.count -= 1


def check_zero(self, i, j, j_pos):
    if j_pos is not None:
        if self.row[i]['items'][j_pos] == 0:
            if self.heap_usage:
                self.remove_from_heap(i, self.row[i]['ind'][j_pos])
            self.remove_by_jpos(i, j_pos)
    else:
        print(555)
        exit(0)
    #     if self.row[i]['items'][j] == 0:
    #         self.remove(i, j)
    #         self.remove_from_heap(i, j)
