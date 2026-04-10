import random
from constants import alpha, beta


def probability(pheromone, distance):
    return (pheromone ** alpha) * ((1 / distance) ** beta)


class Ant:
    def __init__(self, start):
        self.current = start
        self.path = [start]
        self.distance = 0

    def move(self, neighbors):
        probs = []

        # calcular probabilidades
        for node, weight, pheromone in neighbors:
            p = probability(pheromone, weight)
            probs.append(p)

        # normalizar
        total = sum(probs)
        probs = [p / total for p in probs]

        # elegir basado en probabilidad
        choice = random.choices(neighbors, weights=probs)[0]

        next_node, weight, pheromone = choice

        self.path.append(next_node)
        self.distance += weight
        self.current = next_node