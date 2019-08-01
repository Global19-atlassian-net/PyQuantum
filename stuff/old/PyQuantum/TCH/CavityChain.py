class CavityChain:
    def __init__(self, cavities):
        self.cavities = cavities
        self.connections = []

    def cavity(self, id):
        return self.cavities[id]

    def connect(self, id_1, id_2):
        self.connections.append([id_1, id_2])
