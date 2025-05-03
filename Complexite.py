from turtle import lt

import numpy as np
import random
import time
import FlotMax
import Flotmin
from Graphe import Graph
import matplotlib.pyplot as plt
import csv


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
    firsttime = time.perf_counter()
    FlotMax.ford_fulkerson(graphe)
    secondtime = time.perf_counter()
    timeexecution = secondtime - firsttime  # Correction ici
    print(" La durée pour ce graphe avec ford_fulkerson est de  ", timeexecution)
    return timeexecution

def time_execution_push_relabel(graphe):
    firsttime = time.perf_counter()
    FlotMax.push_relabel(graphe)
    secondtime = time.perf_counter()
    timeexecution = secondtime - firsttime  # Correction ici
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
    timeexecution = secondtime - firsttime  # Correction ici
    print(" La durée pour ce graphe avec flot min est de  ", timeexecution)
    return timeexecution


def generer_et_tracer_nuage_de_points(n):
    num_tests = 100
    temps_ford_fulkerson_individual = []
    temps_push_relabel_individual = []
    temps_flot_min_individual = []

    print(f"Génération du graphe pour n = {n}")
    graphe = generate_random_graphe(n)
    
    # Nom du fichier CSV
    filename = f"resultats_n_{n}.csv"

    # Ouvrir le fichier CSV pour écriture
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Itération", "Ford-Fulkerson", "Push-Relabel", "Flot Min"])

        for i in range(1, num_tests + 1):
            tf = time_execution_ford_fulkerson(graphe)
            tp = time_execution_push_relabel(graphe)
            tm = time_execution_flotmin(graphe)

            # Sauvegarder dans les listes pour affichage
            temps_ford_fulkerson_individual.append(tf)
            temps_push_relabel_individual.append(tp)
            temps_flot_min_individual.append(tm)

            # Écrire la ligne dans le fichier CSV
            writer.writerow([i, tf, tp, tm])
            print('-----------------------------', i, "-----------------------------")

    # Nuage de points
    plt.figure(figsize=(10, 6))
    x_values = [n] * num_tests

    plt.scatter(x_values, temps_ford_fulkerson_individual, color='blue', label='Ford-Fulkerson')
    plt.scatter(x_values, temps_push_relabel_individual, color='green', label='Pousser-Réétiqueter')
    plt.scatter(x_values, temps_flot_min_individual, color='red', label='Flot à coût minimal')

    plt.xlabel("Taille du graphe (n)")
    plt.ylabel("Temps d'exécution (secondes)")
    plt.title("Temps d'exécution des algorithmes pour n = {}".format(n))
    plt.legend()
    plt.show()


generer_et_tracer_nuage_de_points(400) # a faire avec tt les nombres demandés