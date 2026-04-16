import random
import constants as const


class Ant:
    def __init__(self, start_node, destination, origin_destination):
        # Nodos físicos
        self.start_node = start_node      # El objeto Nodo original (Tijuana)
        self.current = start_node         # El objeto Nodo donde está parada
        self.current_start_node = start_node # El objeto Nodo donde inició el viaje ACTUAL
        
        # Textos (Nombres de ciudades)
        self.home_city = start_node.name  # "Tijuana"
        self.target_city = destination    # "Chihuahua"
        self.destination = self.target_city # El objetivo del viaje actual ("Chihuahua")
        
        # Estadísticas del viaje
        self.path = [start_node]
        self.distance = 0
        self.found = False
        self.finished = False
        self.steps_limit = const.step_limit
        self.current_step = 0

    def reset_ant(self):
        # Si se pierde o se acaban los pasos, reinicia el viaje desde donde salió
        self.current = self.current_start_node # Es un OBJETO Nodo (no crasheará)
        self.path = [self.current]
        self.distance = 0
        self.current_step = 0
        self.found = False
        self.finished = False

    def return_ant(self):
        # Llegó a su destino. Ahora el inicio es donde está parada...
        self.current_start_node = self.current 
        
        # ...y el nuevo destino es el lado opuesto.
        if self.destination == self.target_city:
            self.destination = self.home_city    # Ahora regresa a Tijuana
        else:
            self.destination = self.target_city  # Ahora va hacia Chihuahua
            
        # Limpiamos la memoria para el nuevo viaje
        self.distance = 0
        self.path = [self.current]
        self.found = False
        self.current_step = 0
        self.finished = False

    def move_independent(self):
        if len(self.path) == 0:
            self.path = [self.current]

        neighbors = self.get_neighbors()

        if not neighbors:
            return False

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