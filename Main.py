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
        filenumber = input("Numéro du fichier (1-5 pour options 1-2, 6-10 pour option 3) : ")
        try:
            filenumber = int(filenumber)
        except ValueError:
            print("Erreur : veuillez entrer un nombre valide.")
            continue

        # Vérification du fichier valide en fonction du choix
        if choice in ['1', '2'] and not (1 <= filenumber <= 5):
            print("Erreur : pour Ford-Fulkerson ou Pousser-Réétiqueter, le fichier doit être entre 1 et 5.")
            continue
        elif choice == '3' and not (6 <= filenumber <= 10):
            print("Erreur : pour Flot à coût minimal, le fichier doit être entre 6 et 10.")
            continue

        # Construction du nom du fichier et création du graphe
        filename = f"Graphe{filenumber}.txt"
        try:
            graph = Graph(filename)
            graph.print_matrices()
        except FileNotFoundError:
            print(f"Erreur : le fichier {filename} n'existe pas.")
            continue
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
            continue

        # Choix de l'algorithme en fonction de l'entrée
        if choice == '1':
            t0 = time.time()
            ford_fulkerson(graph)
            t1 = time.time()
            graph.Finalflot()
        elif choice == '2':
            t0 = time.time()
            push_relabel(graph)
            t1 = time.time()
            graph.Finalflot()
        elif choice == '3':
            try:
                flow_val = int(input("Valeur du flot souhaité : "))
                t0 = time.time()
                # Création du réseau de flot avec la nouvelle classe ReseauFlot
                reseau = ReseauFlot(
                    capacites=graph.c.tolist(),
                    couts=graph.cout.tolist(),
                    noms=graph.noms_sommets(),
                    val_flot=flow_val
                )
                # Résolution du problème de flot à coût minimal
                reseau.resoudre()
                t1 = time.time()
            except ValueError:
                print("Erreur : veuillez entrer une valeur de flot valide.")
                continue
            except AttributeError as e:
                print(f"Erreur : le graphe ne contient pas les informations nécessaires pour le flot à coût minimal. ({e})")
                continue
        
        print(f"Temps d'exécution : {t1 - t0:.4f} s")

if __name__ == '__main__':
    main()