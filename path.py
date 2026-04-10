
class Nodo:
    def _init_(self, name):
        self.name = name


class Path:
    def _init_(self, node_origin:Nodo, weight, node_destination:Nodo, init_feromone):
        self.node_origin = node_origin
        self.node_destination = node_destination
        self.weight = weight
        self.init_feromone = init_feromone