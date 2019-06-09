import numpy as np
import PyQuantum.DarkState.state as state


class Qudit(state.State):
    def __init__(self, dim=2):
        self.dim = dim

        self.base = list(range(dim))
        self.state = np.transpose(np.matrix(np.zeros(self.dim)))

    def set(self, v=0):
        self.state = np.transpose(np.matrix(np.zeros(self.dim)))

        self.state[v] = 1
