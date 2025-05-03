from turtle import lt

import numpy as np
import random
import time
import FlotMax
import Flotmin
from Graphe import Graph
import matplotlib.pyplot as plt



# generer graphe au hasard avec n sommets
def generate_random_graphe(n):  # n représente le nombre de sommets
    # Créer 2 matrices vides, une pour la capacité et une pour le coût
    C = np.zeros((n, n), dtype=int)  # Matrice des capacités
    D = np.zeros((n, n), dtype=int)  # Matrice des coûts

    # On les remplit avec des nombres aléatoires
    for i in range(n):
        for j in range(n):
            if i != j:  # Pas de chiffres sur la diagonale
                C[i][j] = random.randint(1, 100)  # Générer une capacité aléatoire entre 1 et 100
                # Si la capacité est non nulle, on génère un coût aléatoire
                D[i][j] = random.randint(1, 100) if C[i][j] > 0 else 0

    # Créer l'objet graphe
    graphe = Graph(n=n, C=C, D=D)
    graphe.valeur_flot=FlotMax.ford_fulkerson(graphe)# pour flotmin
    return graphe

def time_execution_ford_fulkerson(graphe):
    firsttime= time.perf_counter()
    FlotMax.ford_fulkerson(graphe)
    secondtime=time.perf_counter()
    timeexecution=firsttime-secondtime
    print(" La durée pour ce graphe avec ford_fulkerson est de  ",timeexecution)
    return timeexecution
def time_execution_push_relabel(graphe):
    firsttime = time.perf_counter()
    FlotMax.push_relabel(graphe)
    secondtime = time.perf_counter()
    timeexecution = firsttime - secondtime
    print(" La durée pour ce graphe avec push_relabel est de  ", timeexecution)
    return timeexecution
def time_execution_flotmin(graphe):
    reseau = Flotmin.ReseauFlot(
        capacites=graphe.c.tolist(),
        couts=graphe.cout.tolist(),
        noms=graphe.noms_sommets(),
        val_flot=graphe.valeur_flot

    )
    firsttime = time.perf_counter()


    reseau.resoudre()

    secondtime = time.perf_counter()
    timeexecution = firsttime - secondtime
    print(" La durée pour ce graphe avec flot min est de  ", timeexecution)
    return timeexecution


def generer_et_tracer_nuage_de_points(n):
    num_tests = 100
    # tableau des temps
    temps_ford_fulkerson_individual = []
    temps_push_relabel_individual = []
    temps_flot_min_individual = []

    print(f"Génération du graphe pour n = {n}")
    # nombre aleatoire
    graphe = generate_random_graphe(n)  # Utilise la fonction que tu as écrite

    # Répéter 100 fois le test pour chaque algorithme
    for _ in range(num_tests):
        # on calcule les temps
        temps_ford_fulkerson_individual.append(time_execution_ford_fulkerson(graphe))

        temps_push_relabel_individual.append(time_execution_push_relabel(graphe))


        temps_flot_min_individual.append(time_execution_flotmin(graphe))


    # nuage
    plt.figure(figsize=(10, 6))

    plt.scatter( num_tests, temps_ford_fulkerson_individual, color='blue', label='Ford-Fulkerson')
    plt.scatter( num_tests, temps_push_relabel_individual, color='green', label='Pousser-Réétiqueter')
    plt.scatter( num_tests, temps_flot_min_individual, color='red', label='Flot à coût minimal')

    # Ajouter des labels et un titre
    plt.xlabel("Taille du graphe (n)")
    plt.ylabel("Temps d'exécution (secondes)")
    plt.title("Nuages de points des temps d'exécution par algorithme")
    plt.legend()

    # Afficher le graphique
    plt.show()


generer_et_tracer_nuage_de_points(10) # a faire avec tt les nombres demandés