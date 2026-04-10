class Nodo:
    def __init__(self, name):
        self.name = name


class Path:
    def __init__(self, node_origin, weight, node_destination, init_feromone):
        self.node_origin = node_origin
        self.node_destination = node_destination
        self.weight = weight
        self.pheromone = init_feromone