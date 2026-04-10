import json
from path import Nodo, Path
from constants import init_feromones, evaporation_rate
from ant import Ant


def load_graph():
    with open("world.json") as f:
        data = json.load(f)

    nodes = {}
    paths = []

    for city in data:
        if city not in nodes:
            nodes[city] = Nodo(city)

        for neighbor, dist in data[city]:
            if neighbor not in nodes:
                nodes[neighbor] = Nodo(neighbor)

            paths.append(
                Path(nodes[city], dist, nodes[neighbor], init_feromones)
            )

    return nodes, paths


def get_neighbors(paths, current_node):
    neighbors = []

    for p in paths:
        if p.node_origin == current_node:
            neighbors.append((p.node_destination, p.weight, p.pheromone))

    return neighbors


def main():
    nodes, paths = load_graph()
    target = "Ensenada"

    best_ant_global = None

    for iteracion in range(100):
        ants = [Ant(nodes["Tijuana"]) for _ in range(10)]

        for ant in ants:
            max_steps = 50  

            while ant.current.name != target and max_steps > 0:
                neighbors = get_neighbors(paths, ant.current)

                
                neighbors = [
                    n for n in neighbors if n[0] not in ant.path
                ]

                if not neighbors:
                    break

                ant.move(neighbors)
                max_steps -= 1

            
            if ant.current.name == target:
                print("Ruta:", [n.name for n in ant.path], "Distancia:", ant.distance)

                
                if best_ant_global is None or ant.distance < best_ant_global.distance:
                    best_ant_global = ant

        
        for path in paths:
            path.pheromone *= (1 - evaporation_rate)

    
    if best_ant_global:
        print("\nMEJOR RUTA FINAL:")
        print([n.name for n in best_ant_global.path], "Distancia:", best_ant_global.distance)
    else:
        print("No se encontró ruta al destino")


if __name__ == "__main__":
    main()