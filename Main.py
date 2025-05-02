from Graphe import *
from Flotmin import *
from FlotMax import *
import time

def main():
    print("Projet de Recherche Opérationnelle - Algorithmes de Flot")
    while True:
        print("\nMenu :")
        print("1. Ford-Fulkerson")
        print("2. Pousser-Réétiqueter")
        print("3. Flot à coût minimal")
        print("4. Quitter")
        choice = input("Votre choix : ")
        if choice == '4':
            break
        filenumber = input("Nom du fichier : ")
        filename = "Graphe"+ filenumber +".txt"
        graph = Graph(filename)
        graph.print_matrices()
        if choice == '1':
            t0 = time.time()
            ford_fulkerson(graph)
            t1 = time.time()
        elif choice == '2':
            t0 = time.time()
            push_relabel(graph)
            t1 = time.time()
        elif choice == '3':
            flow_val = int(input("Valeur du flot souhaité : "))
            t0 = time.time()
            min_cost_flow(graph, flow_val)
            t1 = time.time()
        graph.Finalflot()
        print(f"Temps d'exécution : {t1 - t0:.4f} s")

if __name__ == '__main__':
    main()
