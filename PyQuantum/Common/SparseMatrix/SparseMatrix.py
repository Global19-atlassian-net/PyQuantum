# -------------------------------------------------------------------------------------------------
# system
import time
import sys
# -------------------------------------------------------------------------------------------------
# Common
from PyQuantum.Common.Assert import *
# -------------------------------------------------------------------------------------------------
import logging

logging.basicConfig(filename="logs/rank.log", level=logging.DEBUG)
# logging.basicConfig(filename="SparseMatrix/rank.log", level=logging.INFO)


class SparseMatrix:
    from PyQuantum.Common.SparseMatrix.Print import Print, print_row, print_rows
    from PyQuantum.Common.SparseMatrix.Print import to_csv

    from PyQuantum.Common.SparseMatrix.RowsHandler import swap_rows
    from PyQuantum.Common.SparseMatrix.RowsHandler import add_row, remove_row, sub_row
    from PyQuantum.Common.SparseMatrix.RowsHandler import mult_row, divide_row

    from PyQuantum.Common.SparseMatrix.ItemHandler import check_zero
    from PyQuantum.Common.SparseMatrix.ItemHandler import add_item, sub_item
    from PyQuantum.Common.SparseMatrix.ItemHandler import mult_item, div_item

    from PyQuantum.Common.SparseMatrix.ItemHandler import remove, remove_by_jpos, remove_from_heap

    def __init__(self, m=0, n=0, orient='row', heap_usage=False):
        Assert(m >= 0, "m < 0", cf())
        Assert(n >= 0, "n < 0", cf())

        self.m = m
        self.n = n

        self.count = 0

        self.row = dict()
        self.col = dict()

        self.items = dict()
        self.ind = dict()
        self.orient = orient
        self.heap_usage = heap_usage

        self.heap = set()

    def empty(self):
        self.m = 0
        self.n = 0

        self.count = 0

        self.row = dict()
        self.col = dict()

        self.items = dict()
        self.ind = dict()

        if self.heap_usage:
            self.heap = set()

    def add(self, ind, value):
        Assert(len(ind) == 2, "len(ind) != 2", cf())

        i = ind[0]
        j = ind[1]

        Assert(i >= 0, "i < 0", cf())
        Assert(j >= 0, "j < 0", cf())

        if self.n is None:
            self.n = j+1
        else:
            self.n = max(self.n, j+1)

        if self.m is None:
            self.m = i+1
        else:
            self.m = max(self.m, i+1)

        if value == 0:
            return

        if self.orient == 'row':
            if not (i in self.items):
                self.ind[i] = []
                self.items[i] = []
            # --------------------------------------
            inserted = False

            for pos, v in enumerate(self.ind[i]):
                if j < v:
                    self.ind[i].insert(pos, j)
                    self.items[i].insert(pos, value)

                    inserted = True
                    break
                elif j == v:
                    self.items[i][pos] = value
                    inserted = True
                    break

            if not inserted:
                self.ind[i].append(j)
                self.items[i].append(value)
            # --------------------------------------

            if i not in self.row:
                count = 1
            else:
                count = self.row[i]['count'] + 1

            self.row[i] = {
                'ind': self.ind[i],
                'items': self.items[i],
                'count': count
            }
        else:
            if not (j in self.items):
                self.ind[j] = []
                self.items[j] = []

            self.ind[j].append(i)
            self.items[j].append(value)

            self.col[i] = {
                'ind': self.ind[j],
                'items': self.items[j]
            }

        if self.heap_usage:
            self.heap.add(((i, j), value))

        self.count += 1

        return

    def sub_rows(self, i1, i2, jj):
        i1_set = set(self.row[i1]['ind'])
        i2_set = set(self.row[i2]['ind'])

        inter = i1_set & i2_set
        diff = i2_set - i1_set

        for c in inter:
            j_1 = self.row[i1]['ind'].index(c)
            j_2 = self.row[i2]['ind'].index(c)

            v_2 = self.row[i2]['items'][j_2] * self.row[i1]['items'][jj]

            self.sub_item(i1, j_1, v_2, autoremove=False)

        for c in diff:
            j_2 = c
            ind_2 = self.row[i2]['ind'].index(c)

            v_2 = self.row[i2]['items'][ind_2]

            self.add((i1, j_2), -v_2)

        for j_pos in range(len(self.row[i1]['items']))[::-1]:
            self.check_zero(i1, None, j_pos)

        # if i1 in self.row.keys():
        #     for j_pos, j in enumerate(self.row[i1]['items']):
        #         # print(self.row[i1]['items'])
        #         Assert(self.row[i1]['items'][j_pos] != 0,
        #                'nil' + str(self.row[i1]['items']), cf())

        if i1 in self.row.keys():
            self.row[i1]['count'] = len(self.row[i1]['items'])
            size = len(self.row[i1]['items'])
            count = self.row[i1]['count']

            Assert(len(self.row[i1]['items']) == self.row[i1]
                   ['count'], 'count != size(items):' + str(count) + "!=" + str(size) + str(self.row[i1]['items']), cf())

    def get_rows_by_count(self):
        rows_by_count = dict()

        for k, v in self.row.items():
            cnt = v['count']

            if cnt not in rows_by_count.keys():
                rows_by_count[cnt] = []

            rows_by_count[cnt].append(k)

        return rows_by_count

    def rank(self):
        rows_by_count = self.get_rows_by_count()

        divs = 0
        subs = 0

        I = SparseMatrix()
        p = 0

        # for k in sorted(rows_by_count.keys()):
        #     print(k, rows_by_count[k])
        #     for t in rows_by_count[k]:
        #         print(self.row[t])

        while len(rows_by_count) != 0 and self.count != 0:
            p += 1
            # if p > 100:
            # return -1, self, I

            for cnt in sorted(rows_by_count.keys()):
                for row_i in rows_by_count[cnt]:
                    if row_i not in self.row:
                        continue

                    row = self.row[row_i]

                    k = row['items'][0]

                    ind = row['ind'][0]

                    logging.debug("Divide row " + str(row_i) + ' ' +
                                  str(self.row[row_i]) + " on " + str(k))
                    if k == 0:
                        # self.Print(mode='full')
                        self.info()
                    if k != 1:
                        self.divide_row(row_i, k)
                        divs += 1
                        # logging.debug(self.Print(mode='full'))
                        # print('divide ', k)
                        # print('*'*100)
                        # self.Print(mode='full')
                    logging.debug(self.Print(mode='full'))

                    ind = self.row[row_i]['ind'][0]
                    for i1 in list(self.row.keys()):
                        if i1 != row_i and (ind in self.row[i1]['ind']):
                            ind_j = self.row[i1]['ind'].index(ind)
                            j_ind = self.row[row_i]['ind'][0]

                            logging.debug("Sub rows " + str(row_i) + ' -= ' +
                                          str(i1) + " * " + str(ind_j))
                            self.sub_rows(
                                i1, row_i, ind_j)
                            subs += 1
                            print('sub ', k)
                            print('*'*100)
                            self.Print(mode='full')

                    for s in sorted(rows_by_count.keys()):
                        for r in rows_by_count[s]:
                            if r in self.row.keys() and max(self.row[r]['ind']) <= ind:
                                for j_ind, j in enumerate(self.row[r]['ind']):
                                    I.add((r, j),
                                          self.row[r]['items'][j_ind])
                                self.remove_row(r)

                    rows_by_count[cnt].remove(row_i)
                    # time.sleep(2)
                    if rows_by_count[cnt] == []:
                        del rows_by_count[cnt]

        # print('divs = ', divs, ', subs = ', subs, sep='')

        return (len(self.row)+len(I.row)), self, I

    def info(self):
        print('-'*100)
        print('m:', self.m)
        print('n:', self.n)
        print()
        print('count:', self.count)

        if self.count != 0:
            print()

            if self.orient == 'row':
                for i in sorted(self.row.keys()):
                    print('row ', i, ':', sep='')
                    print('\tindex:', self.row[i]['ind'])
                    print('\titems:', self.row[i]['items'])
                    print()
                    print('\tcount:', self.row[i]['count'])
            elif self.orient == 'col':
                for i in sorted(self.col.keys()):
                    print('col ', i, ':', sep='')
                    print('\tindex:', self.col[i]['ind'])
                    print('\titems:', self.col[i]['items'])
                    print('\tcount:', self.row[i]['count'])

        print('-'*100)
        print()

        return

    def __add__(self, k):
        if isinstance(k, float):
            for i in self.row.keys():
                for t in range(len(self.row[i]['items'])):
                    self.row[i]['items'][t] += k
        elif isinstance(k, SparseMatrix):
            other = k

            ind_A = set()
            ind_B = set()

            items_A = set()
            items_B = set()

            all_A = dict()
            all_B = dict()

            for k, v in self.row.items():
                for kj, j in enumerate(v['ind']):
                    ind_A.add((k, j))
                    items_A.add(v['items'][kj])
                    all_A[(k, j)] = v['items'][kj]

            for k, v in other.row.items():
                for kj, j in enumerate(v['ind']):
                    ind_B.add((k, j))
                    items_B.add(v['items'][kj])
                    all_B[(k, j)] = v['items'][kj]

            diff = ind_A ^ ind_B
            intersection = ind_A & ind_B

            C = SparseMatrix(
                m=max(self.m, other.m),
                n=max(self.n, other.n),
                orient='row'
            )

            for i in diff:
                if i in all_A.keys():
                    C.add((i[0], i[1]), all_A[(i[0], i[1])])
                elif i in all_B.keys():
                    C.add((i[0], i[1]), all_B[(i[0], i[1])])

            for i in intersection:
                C.add((i[0], i[1]), all_A[(i[0], i[1])] + all_B[(i[0], i[1])])

            return C

        return self

    def __sub__(self, k):
        if isinstance(k, float):
            return self.__add__(-k)
        elif isinstance(k, SparseMatrix):
            return self.__add__(k * -1)

    def __mul__(self, k):
        for i in self.row.keys():
            for t in range(len(self.row[i]['items'])):
                self.row[i]['items'][t] *= k

        return self

    def __truediv__(self, k):
        Assert(k != 0, "k == 0", cf())

        return self.__mul__(1.0 / k)
