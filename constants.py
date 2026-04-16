import networkx as nx
import json

with open("world.json", "r", encoding="utf-8") as worldFile:
    world = json.load(worldFile)

nodes_directory = {}
paths_list = []

#independent_mode
init_feromones = 0.5        #feromona inicial de cada camino
min_pheromone = 0.1         #tope minimo de feromonas para cada camino
evaporation_rate = 0.07      #coheficiente de evaporacion de la feromona
alpha = 2                   #importancia de feromona
beta = 1                    #importancia de distancia
velocidad = 0.001             #velocidad de la simulacion
init_city = "Tijuana"
final_city = "Sonoyta"
n_iterations = 200


#not_independent_mode
init_feromones_ = 0.1        #feromona inicial de cada camino
min_pheromone_ = 0.1         #tope minimo de feromonas para cada camino
evaporation_rate_ = 0.8      #coheficiente de evaporacion de la feromona
alpha_ = 2                   #importancia de feromona
beta_ = 2                    #importancia de distancia
velocidad_ = 0.1             #velocidad de la simulacion
init_city_ = "Tijuana"
final_city_ = "Chihuahua"
n_iterations_ = 20


#Ants constanst
n_ants = 10
step_limit = 50

animations = False
mode_independent = True

G = nx.Graph()

CITY_POSITIONS = {
    "Tijuana": (-117.5, 33.0), "Tecate": (-116.6, 33.5), "Mexicali": (-115.4, 32.6),
    "Rosarito": (-117.5, 31.5), "Ensenada": (-116.6, 31.5), "San Felipe": (-114.8, 31.0),
    "San Quintin": (-115.9, 30.4), "Guerrero Negro": (-114.0, 28.0), "Santa Rosalia": (-112.2, 27.3),
    "Mulege": (-111.9, 26.9), "Ciudad Constitucion": (-111.6, 25.0), "San Carlos": (-112.9, 24.8),
    "La Paz": (-110.3, 24.1), "San Jose del Cabo": (-109.7, 21.9), "Cabo San Lucas": (-110.9, 22.9),
    "San Luis Rio Colorado": (-114.7, 32.4), "Sonoyta": (-112.8, 31.8), "Puerto Penasco": (-113.5, 31.3),
    "Caborca": (-112.1, 30.7), "Santa Ana": (-111.1, 30.5), "Nogales": (-110.9, 31.3),
    "Cananea": (-110.2, 30.9), "Agua Prieta": (-109.5, 31.3), "Hermosillo": (-110.9, 29.0),
    "Guaymas": (-110.9, 27.9), "Ciudad Obregon": (-109.9, 27.4), "Moctezuma": (-109.6, 29.8),
    "Yécora": (-108.9, 28.3), "Janos": (-108.1, 30.8),
    "Ciudad Juarez": (-106.4, 31.7), "Villa Ahumada": (-106.5, 30.6), "Flores Magon": (-107.4, 29.8),
    "Sueco": (-106.4, 29.8), "Chihuahua": (-106.0, 28.6), "Ojinaga": (-104.4, 29.5),
    "Delicias": (-105.4, 28.1), "Ciudad Jimenez": (-104.9, 27.1), "Parral": (-105.6, 26.9),
    "Ciudad Cuauhtemoc": (-106.8, 28.4)
}
