import random
import constants as const


class Ant:
    def __init__(self, start_node):
        self.current = start_node
        self.path = [start_node]
        self.distance = 0
        self.finished = False

    def get_neighbors(self):
        neighbors = []
        for p in const.paths_list:
            # Buscamos conexiones desde el nodo actual
            if p.node_origin == self.current:
                # Solo considerar nodos NO visitados
                if p.node_destination not in self.path:
                    neighbors.append(p)
        return neighbors

    def move(self):
        neighbors = self.get_neighbors()
        
        if not neighbors:
            self.finished = True # Ya no tiene a dónde ir
            return False

        probs = []
        for p in neighbors:
            # Usamos los atributos del objeto Path directamente
            prob = (p.pheromone ** const.alpha) * ((1.0 / p.weight) ** const.beta)
            probs.append(prob)

        total = sum(probs)
        if total == 0: # Caso borde: todas las opciones son despreciables
            self.finished = True
            return False

        normalized_probs = [p / total for p in probs]

        # Elegimos el OBJETO Path ganador
        chosen_path = random.choices(neighbors, weights=normalized_probs)[0]

        # Actualizamos estado de la hormiga
        self.current = chosen_path.node_destination
        self.path.append(self.current)
        self.distance += chosen_path.weight
        return True