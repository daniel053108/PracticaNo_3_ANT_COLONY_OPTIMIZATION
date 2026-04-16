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

    print("[")
    for p in final_path:
        print(p.name)
        print("     |")
        print("     V")
    
    print("]")

    # Mostramos el mapa final
    print("Generando visualización...")
    utils.final_View()


if __name__ == "__main__":
    main()