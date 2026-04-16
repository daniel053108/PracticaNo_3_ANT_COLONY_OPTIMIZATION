import world_utils as utils
import constants as const

def main():
    print("--- Iniciando Sistema ACO ---")
    utils.load_graph()     # Lee el JSON y crea objetos Path
    utils.create_grafo()    # Inicializa el objeto NetworkX


    # Ejecutamos la simulación (Ej: 20 iteraciones, 10 hormigas por vez)
    print("Simulando búsqueda de rutas...")
    if const.mode_independent:
        utils.run_aco_ant_independent_simulation(iterations=const.n_iterations, n_ants=const.n_ants)
    else:
        utils.run_aco_simulation(iterations=const.n_iterations_, n_ants=const.n_ants)
    
    final_path = utils.get_final_path()

    total_distance = 0

    for i in range(len(final_path)):
        print(final_path[i].name)

        if i < len(final_path) - 1:
            u = final_path[i]
            v = final_path[i + 1]

            for p in const.paths_list:
                if p.node_origin == u and p.node_destination == v:
                    total_distance += p.weight
                    break

    

    print("[")
    for p in final_path:
        print(p.name)
        print("     |")
        print("     V")
    
    print("]")
    print("\n Distancia total:", total_distance)
   

    # Mostramos el mapa final
    print("Generando visualización...")
    utils.final_View(final_path)


if __name__ == "__main__":
    main()