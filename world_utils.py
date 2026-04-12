import constants as const
from path import Nodo, Path
from ant import Ant  # <--- ASEGÚRATE DE IMPORTAR TU CLASE ANT
import networkx as nx
import matplotlib.pyplot as plt

def load_graph():
    # Evitar duplicados si se llama varias veces
    const.paths_list = []
    
    for city in const.world:
        if city not in const.nodes_directory:
            const.nodes_directory[city] = Nodo(city)

        for neighbor, dist in const.world[city]:
            if neighbor not in const.nodes_directory:
                const.nodes_directory[neighbor] = Nodo(neighbor)

            # Creamos ambos sentidos para que la hormiga pueda ir y volver
            const.paths_list.append(
                Path(const.nodes_directory[city], dist, const.nodes_directory[neighbor], const.init_feromones)
            )
            const.paths_list.append(
                Path(const.nodes_directory[neighbor], dist, const.nodes_directory[city], const.init_feromones)
            )

def create_grafo():
    const.G.clear() # Limpiar antes de crear
    for path in const.paths_list:
        origin = path.node_origin.name
        dest = path.node_destination.name
        const.G.add_edge(origin, dest, weight=path.weight, pheromone=path.pheromone)

def update_pheromones(ants):
    # 1. EVAPORACIÓN
    for p in const.paths_list:
        p.pheromone *= (1 - const.evaporation_rate)
        if p.pheromone < const.min_pheromone: p.pheromone = const.min_pheromone

    # 2. DEPÓSITO
    for ant in ants:
        # IMPORTANTE: Que el destino sea el mismo que en la simulación
        if ant.current.name == const.final_city:  
            reward = 1000 / ant.distance  # Aumenté el reward para que sea más notable
            for i in range(len(ant.path) - 1):
                u = ant.path[i]
                v = ant.path[i+1]
                for p in const.paths_list:
                    if p.node_origin == u and p.node_destination == v:
                        p.pheromone += reward

def refresh_graph_data():
    for p in const.paths_list:
        # Actualizamos la feromona en las aristas de NetworkX
        if const.G.has_edge(p.node_origin.name, p.node_destination.name):
            const.G[p.node_origin.name][p.node_destination.name]['pheromone'] = p.pheromone

def run_aco_simulation(iterations, n_ants):
    plt.ion() # Activar modo interactivo de Matplotlib
    plt.show() # Mostrar ventana vacía
    
    start_node = const.nodes_directory[const.init_city]
    
    for i in range(iterations):
        colony = [Ant(start_node) for _ in range(n_ants)]
        
        # Simulamos el movimiento paso a paso para TODA la colonia a la vez
        # (Esto se ve mejor que mover una por una hasta el final)
        active_ants = True
        step = 0
        while active_ants and step < 50:
            active_ants = False
            for ant_idx, ant in enumerate(colony):
                if not ant.finished:
                    if ant.move():
                        active_ants = True
                        if ant.current.name == const.final_city:
                            ant.finished = True
                    else:
                        ant.finished = True # Atrapada

            # DIBUJAR EL MOVIMIENTO DE ESTE PASO
            draw_current_state(colony, i+1, step)
            step += 1

        # Al final de la iteración, actualizamos feromonas y datos
        update_pheromones(colony)
        refresh_graph_data() 
        
        # (Opcional) Dibujar un frame final de la iteración con grosores actualizados
        draw_current_state([], i+1, step) 
        plt.pause(0.5) # Pausa más larga entre iteraciones

    plt.ioff() # Desactivar modo interactivo
    print("Simulación completada.")
    plt.show() # Mantener ventana abierta
    
def draw_current_state(ants, current_iteration, current_ant_idx):
    plt.clf()  # Limpiar frame anterior
    
    pos = {
        city: (coords[0] * 2, coords[1] * 2) 
        for city, coords in const.CITY_POSITIONS.items() 
        if city in const.G.nodes()
    }

    # 1. Dibujar la infraestructura (Caminos y Ciudades)
    # Usamos grosores basados en feromona actual
    feromonas = [const.G[u][v].get('pheromone', 1) for u, v in const.G.edges()]
    widths = [min(10.0,0.5 + (f * 1.0)) for f in feromonas]
    edge_labels = nx.get_edge_attributes(const.G, 'weight')
    
    nx.draw_networkx_edges(const.G, pos, width=widths, edge_color="#150E0E", alpha=0.5)
    nx.draw_networkx_nodes(const.G, pos, node_size=600, node_color='white', edgecolors='black')
    nx.draw_networkx_labels(const.G, pos, font_size=7)

    nx.draw_networkx_edge_labels(
        const.G, 
        pos, 
        edge_labels=edge_labels, 
        font_size=6,      # Tamaño pequeño para que no estorbe
        font_color='red', # Color llamativo para diferenciarlo del mapa
        label_pos=0.5     # 0.5 es justo en medio de la línea
    )

    # 2. DIBUJAR LAS HORMIGAS (Puntos Rojos)
    # Extraemos la posición (X, Y) de la ciudad actual de cada hormiga activa
    ant_positions = []
    for ant in ants:
        # Solo dibujamos hormigas que no han terminado y tienen posición válida
        if not ant.finished and ant.current.name in pos:
            ant_positions.append(pos[ant.current.name])
    
    if ant_positions:
        # Convertimos la lista de tuplas (X,Y) en dos listas [X] y [Y] para scatter
        x_coords, y_coords = zip(*ant_positions)
        plt.scatter(x_coords, y_coords, color='red', s=80, label='Hormigas', zorder=10)

    # Info de la simulación
    plt.title(f"ACO en Vivo - Iteración: {current_iteration} | Hormiga: {current_ant_idx+1}")
    plt.axis('off')
    
    plt.draw()
    plt.pause(const.velocidad) #CONTROL DE VELOCIDAD POR PASO (0.05s es rápido pero visible)

def run_simulation(iteration_name=""):
    plt.clf()  # Limpiar la figura actual para el siguiente frame
    
    pos = {
        city: (coords[0] * 2, coords[1] * 2) 
        for city, coords in const.CITY_POSITIONS.items() 
        if city in const.G.nodes()
    }

    # Calculamos grosores basados en feromona actual
    feromonas = [const.G[u][v].get('pheromone', 1) for u, v in const.G.edges()]
    widths = [0.5 + (f * 1.5) for f in feromonas] # Ajuste de grosor

    # Dibujamos
    # Dentro de run_simulation:
    edge_colors = [const.G[u][v]['pheromone'] for u, v in const.G.edges()]
    # Usará un mapa de color de Amarillo a Rojo (YlOrRd)
    nx.draw_networkx_edges(const.G, pos, width=widths, edge_color=edge_colors, edge_cmap=plt.cm.YlOrRd, alpha=0.7)
    nx.draw_networkx_nodes(const.G, pos, node_size=600, node_color='white', edgecolors='black')
    nx.draw_networkx_labels(const.G, pos, font_size=7)

    plt.title(f"Simulación ACO - {iteration_name}")
    plt.axis('off')
    
    plt.draw()        # Dibujar sin bloquear
    plt.pause(const.velocidad)    