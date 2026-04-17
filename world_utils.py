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
                Path(const.nodes_directory[city], dist, const.nodes_directory[neighbor], 
                     const.init_feromones if const.mode_independent else const.init_feromones_)
            )
            const.paths_list.append(
                Path(const.nodes_directory[neighbor], dist, const.nodes_directory[city], 
                     const.init_feromones if const.mode_independent else const.init_feromones_)
            )

def create_grafo():
    const.G.clear() # Limpiar antes de crear
    for path in const.paths_list:
        origin = path.node_origin.name
        dest = path.node_destination.name
        const.G.add_edge(origin, dest, weight=path.weight, pheromone=path.pheromone)

def update_pheromones(ants):
    #EVAPORACIÓN
    for p in const.paths_list:
        p.pheromone *= (1 - const.evaporation_rate_)
        if p.pheromone < const.min_pheromone_: p.pheromone = const.min_pheromone_

    #DEPÓSITO
    for ant in ants:
        if ant.current.name == ant.destination:  
            reward = (1 / ant.distance) * 100
            for i in range(len(ant.path) - 1):
                u = ant.path[i]
                v = ant.path[i+1]
                for p in const.paths_list:
                    if p.node_origin == u and p.node_destination == v or (p.node_origin == v and p.node_destination == u):
                        p.pheromone = min(10, p.pheromone + reward)

def refresh_graph_data():
    for p in const.paths_list:
        # Actualizamos la feromona en las aristas de NetworkX
        if const.G.has_edge(p.node_origin.name, p.node_destination.name):
            const.G[p.node_origin.name][p.node_destination.name]['pheromone'] = p.pheromone

def insert_pheromone_in_path(ant):
    if ant.current.name == ant.destination:  
        reward = (1000 / ant.distance)
        for i in range(len(ant.path) - 1):
            u = ant.path[i]
            v = ant.path[i+1]
            for p in const.paths_list:
                if p.node_origin == u and p.node_destination == v or (p.node_origin == v and p.node_destination == u):
                    p.pheromone = min(10, p.pheromone + reward)
                    print(p.pheromone)  

def evaporate_pheromone():
    for p in const.paths_list:
        p.pheromone *= (1 - const.evaporation_rate)
        if p.pheromone < const.min_pheromone: p.pheromone = const.min_pheromone   

def run_aco_ant_independent_simulation(iterations, n_ants):
    plt.ion()
    plt.show()

    start_node = const.nodes_directory[const.init_city]
    
    colony = [Ant(start_node, destination=const.final_city, origin_destination=const.final_city) for _ in range(n_ants)]

    for i in range(iterations):
        for ant_idx, ant in enumerate(colony):
            if ant.current_step >= ant.steps_limit:
                ant.reset_ant()

            if ant.found:
                insert_pheromone_in_path(ant)
                refresh_graph_data() 
                ant.return_ant()

            if not ant.move_independent():
                ant.reset_ant()       
            
            refresh_graph_data() 
            if const.animations:
                draw_current_state(colony, current_iteration=i+1)

        evaporate_pheromone()
        refresh_graph_data() 
    
    plt.ioff() # Desactivar modo interactivo
    print("Simulación completada.")

def run_aco_simulation(iterations, n_ants):
    plt.ion() # Activar modo interactivo de Matplotlib
    plt.show() # Mostrar ventana vacía
    
    start_node = const.nodes_directory[const.init_city]
    
    for i in range(iterations):
        colony = [Ant(start_node, const.final_city, const.final_city) for _ in range(n_ants)]

        active_ants = True
        step = 0
        while active_ants and step < 50:
            active_ants = False

            for ant_idx, ant in enumerate(colony):
                if not ant.finished:
                    if ant.move():
                        active_ants = True
                        if ant.current.name == ant.destination:
                            ant.finished = True
                    else:
                        ant.finished = True

            # DIBUJAR EL MOVIMIENTO DE ESTE PASO
            if const.animations:
                draw_current_state_(colony, i+1, step)
            step += 1

        # Al final de la iteración, actualizamos feromonas y datos
        update_pheromones(colony)
        refresh_graph_data() 
        
        plt.pause(const.velocidad) # Pausa más larga entre iteraciones

    plt.ioff() # Desactivar modo interactivo
    print("Simulación completada.")
    
def draw_current_state(ants, current_iteration = 0):
    plt.clf()  # Limpiar frame anterior

    pos = {
        city: (coords[0] * 2, coords[1] * 2) 
        for city, coords in const.CITY_POSITIONS.items() 
        if city in const.G.nodes()
    }

    # Usamos grosores basados en feromona actual
    feromonas = [const.G[u][v].get('pheromone', const.init_feromones) for u, v in const.G.edges()]
    widths = [min(10.0, 0.5 + (f * 10.0)) if f >= 0 else const.init_feromones for f in feromonas]
    edge_labels = nx.get_edge_attributes(const.G, 'weight')
    nx.draw_networkx_edges(const.G, pos, width=widths, edge_color=feromonas, edge_cmap=plt.cm.YlOrRd, edge_vmax=1, edge_vmin=0)
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

    ant_positions = []
    for ant in ants:
        if ant.current.name in pos:
            ant_positions.append(pos[ant.current.name])
    
    if ant_positions:
        x_coords, y_coords = zip(*ant_positions)
        plt.scatter(x_coords, y_coords, color='red', s=80, label='Hormigas', zorder=10)

    plt.title(f"ACO en Vivo - Iteración: {current_iteration}")
    plt.axis('off')
    
    plt.draw()
    plt.pause(const.velocidad)

def draw_current_state_(ants, current_iteration = 0, current_ant_idx = 0):
    plt.clf()  # Limpiar frame anterior

    pos = {
        city: (coords[0] * 2, coords[1] * 2) 
        for city, coords in const.CITY_POSITIONS.items() 
        if city in const.G.nodes()
    }

    # Usamos grosores basados en feromona actual
    feromonas = [const.G[u][v].get('pheromone', const.init_feromones_) for u, v in const.G.edges()]
    widths = [min(10.0, 0.5 + (f * 10.0)) if f >= 0 else const.init_feromones_ for f in feromonas]
    edge_labels = nx.get_edge_attributes(const.G, 'weight')
    nx.draw_networkx_edges(const.G, pos, width=widths, edge_color=feromonas, edge_cmap=plt.cm.YlOrRd, edge_vmax=1, edge_vmin=0)
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

    ant_positions = []
    for ant in ants:
        if ant.current.name in pos:
            ant_positions.append(pos[ant.current.name])
    
    if ant_positions:
        x_coords, y_coords = zip(*ant_positions)
        plt.scatter(x_coords, y_coords, color='red', s=80, label='Hormigas', zorder=10)

    plt.title(f"ACO en Vivo - Iteración: {current_iteration} | Paso: {current_ant_idx+1}")
    plt.axis('off')
    
    plt.draw()
    plt.pause(const.velocidad)

def get_best_neighbor(node, visited_nodes):
    # Filtramos: el destino NO debe estar en la lista de visitados
    neighbors = [
        {"node": p.node_destination, "pheromone": p.pheromone} 
        for p in const.paths_list 
        if p.node_origin == node and p.node_destination not in visited_nodes
    ]
    
    if not neighbors:
        return None

    # Retorna el que tiene más feromona
    return max(neighbors, key=lambda n: n["pheromone"])

def get_final_path():
    id_inicio = const.init_city 
    id_final = const.final_city 
    
    node = const.nodes_directory[id_inicio]
    target_node = const.nodes_directory[id_final]
    
    
    final_path = [node]
    
    while node != target_node:
        
        best_data = get_best_neighbor(node, final_path)
        
        if not best_data:
            print(f"Camino interrumpido en {node.name}: no hay vecinos no visitados.")
            break
            
        node = best_data["node"]
        final_path.append(node)
        
    return final_path

def final_View(final_path=None, iteration_name=""):
    plt.clf() 
    
    pos = {
        city: (coords[0] * 2, coords[1] * 2) 
        for city, coords in const.CITY_POSITIONS.items() 
        if city in const.G.nodes()
    }

    feromonas = [const.G[u][v].get('pheromone', 0.1) for u, v in const.G.edges()]
    widths = [min(10,0.5 + (f * 10.0)) for f in feromonas]

    nx.draw_networkx_edges(const.G, pos, width=widths, edge_color=feromonas, edge_cmap=plt.cm.YlOrRd, edge_vmax=1, edge_vmin=0)
    nx.draw_networkx_nodes(const.G, pos, node_size=600, node_color='white', edgecolors='black')
    nx.draw_networkx_labels(const.G, pos, font_size=7)

    plt.subplots_adjust(right=0.7)

    if final_path:
        total_distance = 0
        
        if final_path:
            for i in range(len(final_path) - 1):
                u = final_path[i]
                v = final_path[i + 1]

                for p in const.paths_list:
                    if p.node_origin == u and p.node_destination == v:
                        total_distance += p.weight
                        break

        ciudades = [n.name for n in final_path]
        
        texto = "Ruta final:\n\n"
        for i, ciudad in enumerate(ciudades):
            texto += f"{i+1}. {ciudad}\n"

        

        texto += f"\n Distancia total: {total_distance}"
        
        plt.text(
            1.05, 0.5,  
            texto,
            transform=plt.gca().transAxes,
            fontsize=9,
            verticalalignment='center',
            bbox=dict(facecolor='white', alpha=0.8)
        )

    plt.title(f"Simulación ACO FINALIZADA - {iteration_name}")
    plt.axis('off')
    
    print("Mostrando mapa final. Cierra la ventana para terminar...")
    plt.show(block=True)