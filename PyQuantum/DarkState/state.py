import numpy as np
import itertools


class State:
    def __init__(self, state, base):
        self.state = state
        self.base = base

    def tensor(self, other):
        state = np.kron(self.state, other.state)
        bbase = None
        # self.state = state
        # print('self.base:', self.base)
        # print('other.base:', other.base)
        if isinstance(self.base, list):
            bbase = tuple(self.base)

        if isinstance(other.base, list):
            other.base = tuple(other.base)
            # print(other.base)
            # exit(0)

        # self.base = tuple((t1, t2)
        #                   for t1 in tuple(self.base) for t2 in tuple(other.base))
        # # self.base = itertools.product(self.base, other.base)
        # # self.base = list(self.base)
        # # self.base = list(map(list, self.base))
        # # self.base = np.array(self.base)
        base = []
        # print(bbase)
        for v1 in bbase:
            for v2 in other.base:
                if isinstance(v1, list) and not isinstance(v2, list):
                    base.append(v1+[v2])
                elif not isinstance(v1, list) and isinstance(v2, list):
                    base.append([v1]+v2)
                else:
                    base.append([v1, v2])

        # self.base = base
        # print(state)
        # print(base)

        return State(state=state, base=base)

        # self.base = list(self.base)
        # print("\n\nBasee:")
        # print(self.base)
        # self.base = np.kron(self.base, other.base)
        # print('self.base:', self.base)

    def __add__(self, other):
        self.state += other.state

        return self

    def __eq__(self, other):
        print(123)

    def print_base(self):
        # print('Base: ', end='')

        # print(self.base)
        # exit(0)
        if isinstance(self.base[0], list):
            base = []

            for v in self.base:
                base += [''.join([str(elem) for elem in v])]

            print(','.join(['|'+str(i)+'>' for i in base]))
        else:
            print(','.join(['|'+str(i)+'>' for i in self.base]))
