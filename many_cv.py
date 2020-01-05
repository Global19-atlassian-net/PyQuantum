class BaseCavity:
    def __init__(self, wc):
        pass


class TCCavity(BaseCavity):
    def __init__(self, wc, wa, g, n_atoms, n_levels=2):
        BaseCavity.__init__(self, wc)
        pass


cv = BaseCavity(wc=1)

cv = TCCavity(wc=1, wa=1, g=1, n_atoms=1, n_levels=2)

print(123)
