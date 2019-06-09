import PyQuantum.DarkState.qudit as qudit
from PyQuantum.DarkState.state import *


def sigma(perm):
    rate = 0

    size = len(perm)

    for i in range(size-1):
        for j in range(i, size):
            rate += int(perm[i] > perm[j])

    return (rate % 2)


class DarkState(State):
    def __init__(self, perm, n_levels, base=None):
        State = None

        if base is None:
            self.base = list(range(n_levels))
        else:
            self.base = base

        for i in perm:
            q = qudit.Qudit(dim=n_levels)
            # print("i =", i)
            q.set(int(i))

            if State is None:
                State = q
            else:
                State = State.tensor(q)

        if sigma(perm) == 1:
            State.state *= -1

        # self.base = State.base
        self.state = State.state
        # self = State

    def print(self, style='dirac'):
        sub = "₀₁₂₃₄₅₆₇₈₉"

        for k, v in enumerate(self.base):
            ampl = self.state[k, 0]
            if ampl == 1.0:
                ampl = ''
            elif ampl < 0:
                ampl = '-'

            if ampl != 0:
                if isinstance(v, list):
                    base = [''.join([str(elem) for elem in v])]

                    brack = []

                    # print(''.join([ampl + '|'+str(i)+'>' for i in base]))
                    # print([sub[k] for k in range(len(base))])
                    for v in base:
                        for t in v:
                            brack.append('|'+self.state[k, 0]+'⟩'+sub[int(t)])
                            # print()
                    print(ampl, ''.join(brack), sep='')
                else:
                    print(ampl, '|', v, sub[k], '⟩', sep='', end='')

        print()

        return
