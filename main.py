import world_utils as utils
import constants as const

def main():
    print("--- Iniciando Sistema ACO ---")
    utils.load_graph()     # Lee el JSON y crea objetos Path
    utils.create_grafo()    # Inicializa el objeto NetworkX


    # Ejecutamos la simulación (Ej: 20 iteraciones, 10 hormigas por vez)
    print("Simulando búsqueda de rutas...")
    utils.run_aco_simulation(iterations=20, n_ants=10)
    
    # Mostramos el mapa final
    print("Generando visualización...")
    utils.run_simulation()


if __name__ == "__main__":
    main()