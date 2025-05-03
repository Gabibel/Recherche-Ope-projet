from turtle import lt

import numpy as np
import random
import time
import FlotMax
import Flotmin
from Graphe import Graph
import matplotlib.pyplot as plt
import csv
import pandas as pd

def generate_random_graphe(n): 
    C = np.zeros((n, n), dtype=int)  
    D = np.zeros((n, n), dtype=int)  

    for i in range(n):
        for j in range(n):
            if i != j:  
                C[i][j] = random.randint(1, 100)  
                D[i][j] = random.randint(1, 100) if C[i][j] > 0 else 0

    graphe = Graph(n=n, C=C, D=D)
    graphe.valeur_flot=FlotMax.ford_fulkerson(graphe)
    return graphe

def time_execution_ford_fulkerson(graphe):
    firsttime = time.perf_counter()
    FlotMax.ford_fulkerson(graphe)
    secondtime = time.perf_counter()
    timeexecution = secondtime - firsttime  
    print(" La durée pour ce graphe avec ford_fulkerson est de  ", timeexecution)
    return timeexecution

def time_execution_push_relabel(graphe):
    firsttime = time.perf_counter()
    FlotMax.push_relabel(graphe)
    secondtime = time.perf_counter()
    timeexecution = secondtime - firsttime  
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
    timeexecution = secondtime - firsttime  
    print(" La durée pour ce graphe avec flot min est de  ", timeexecution)
    return timeexecution


def generer_et_tracer_nuage_de_points(n):
    num_tests = 100
    temps_ford_fulkerson_individual = []
    temps_push_relabel_individual = []
    temps_flot_min_individual = []

    print(f"Génération du graphe pour n = {n}")
    graphe = generate_random_graphe(n)
    
    
    filename = f"resultats_n_{n}.csv"

    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Itération", "Ford-Fulkerson", "Push-Relabel", "Flot Min"])

        for i in range(1, num_tests + 1):
            tf = time_execution_ford_fulkerson(graphe)
            tp = time_execution_push_relabel(graphe)
            tm = time_execution_flotmin(graphe)

            
            temps_ford_fulkerson_individual.append(tf)
            temps_push_relabel_individual.append(tp)
            temps_flot_min_individual.append(tm)

            
            writer.writerow([i, tf, tp, tm])
            print('-----------------------------', i, "-----------------------------")

    
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


#generer_et_tracer_nuage_de_points(400)


fichiers_csv = [
    "resultats_n_10.csv",
    "resultats_n_20.csv",
    "resultats_n_40.csv",
    "resultats_n_100.csv",
    "resultats_n_400.csv"
]


n_values = []
max_ford_fulkerson = []
max_push_relabel = []
max_flot_min = []


for fichier in fichiers_csv:

    n = int(fichier.split("_")[2].split(".")[0])
    n_values.append(n)
    data = pd.read_csv(fichier, encoding="latin1")
    max_ford_fulkerson.append(data["Ford-Fulkerson"].max())
    max_push_relabel.append(data["Push-Relabel"].max())
    max_flot_min.append(data["Flot Min"].max())


plt.figure(figsize=(10, 6))
plt.plot(n_values, max_ford_fulkerson, label="Ford-Fulkerson", marker="o", color="blue")
plt.plot(n_values, max_push_relabel, label="Push-Relabel", marker="o", color="green")
plt.plot(n_values, max_flot_min, label="Flot Min", marker="o", color="red")

plt.xlabel("Taille du graphe (n)")
plt.ylabel("Temps d'exécution maximal (secondes)")
plt.title("Temps d'exécution maximal des algorithmes en fonction de n")
plt.legend()
plt.grid()
plt.show()