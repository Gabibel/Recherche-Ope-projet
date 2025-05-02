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

        # Quitter si l'utilisateur choisit l'option 4
        if choice == '4':
            break

        # Demander le numéro du fichier
        filenumber = input("Nom du fichier (1 à 5 pour Ford-Fulkerson et Pousser-Réétiqueter, 6 à 10 pour Flot à coût minimal) : ")
        filenumber = int(filenumber)  # Convertir en entier

        # Vérification du fichier valide en fonction du choix
        if choice in ['1', '2'] and not (1 <= filenumber <= 5):
            print("Erreur : pour Ford-Fulkerson ou Pousser-Réétiqueter, le fichier doit être entre 1 et 5.")
            continue
        elif choice == '3' and not (6 <= filenumber <= 10):
            print("Erreur : pour Flot à coût minimal, le fichier doit être entre 6 et 10.")
            continue

        # Construction du nom du fichier et création du graphe
        filename = f"Graphe{filenumber}.txt"
        graph = Graph(filename)
        graph.print_matrices()

        # Choix de l'algorithme en fonction de l'entrée
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
