import random
import constants as const


class Ant:
    def __init__(self, start_node, destination, origin_destination):
        self.start_node = start_node
        self.current = start_node
        self.path = [start_node]
        self.return_path = [start_node]
        self.distance = 0
        self.found = False
        self.returned = False
        self.destination = destination
        self.origin_destination = origin_destination
        self.steps_limit = const.step_limit
        self.current_step = 0
        self.finished = False

    def reset_ant(self):
        self.current = self.start_node
        self.path = [self.start_node]
        self.distance = 0
        self.current_step = 0
        self.return_path = [self.start_node]
        self.found = False
        self.returned = False

    def return_ant(self):
        if self.returned:
            self.returned = False
            self.destination = self.origin_destination
        else:
            self.destination = self.start_node.name
            self.returned = True
        self.current_step = 0
        self.distance = 0
        self.path = []
        self.found = False

    def move_independent(self):
        if len(self.path) == 0:
            self.path = [self.current]

        neighbors = self.get_neighbors()

        if not neighbors:
            return False
        
        if self.returned:
            self.return_path.pop()
            
            target_node = self.return_path[-1]
            path = None
            for p in const.paths_list:
                if self.current == p.node_origin and target_node == p.node_destination:
                    path = p
                    break
            self.current = target_node
            self.path.append(self.current)
            self.distance += path.weight
            self.current_step += 1
            if self.current.name == self.destination:
                self.found = True
            return True

        probs = []
        for p in neighbors:
            # Usamos los atributos del objeto Path directamente
            prob = (p.pheromone ** const.alpha) * ((1.0 / p.weight) ** const.beta)
            probs.append(prob)

        total = sum(probs)
        if total == 0: # Caso borde: todas las opciones son despreciables
            return False

        normalized_probs = [p / total for p in probs]

        chosen_path = random.choices(neighbors, weights=normalized_probs)[0]

        self.current = chosen_path.node_destination
        self.path.append(self.current)
        if not self.returned:
            self.return_path.append(self.current)
        self.distance += chosen_path.weight
        self.current_step += 1
        if self.current.name == self.destination:
            self.found = True
        return True


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