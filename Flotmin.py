def bellman_ford(graphe, distances, parent):
    for i in range(graphe.n):
        distances[i] = float('inf')
        parent[i] = -1
    distances[graphe.source] = 0
    for j in range(graphe.n - 1):
        for u in range(graphe.n):
            for v in range(graphe.n):
                if graphe.reste[u][v] > 0 and distances[v] > distances[u] + graphe.cout[u][v]:
                    distances[v] = distances[u] + graphe.cout[u][v]
                    parent[v] = u
    return distances

def min_cost_flow(graphe, desired_flow):
    print("\nDébut de l'algorithme de flot à coût minimal")
    initial_flow = sum(graphe.c[graphe.source])
    if desired_flow > initial_flow:
        print("Flot demandé supérieur au flot max.")
        return
    graphe.flot = graphe.flot * 0
    graphe.reste = graphe.c.copy()
    current_flow = 0
    total_cost = 0
    while current_flow < desired_flow:
        distances = [float('inf')] * graphe.n
        parent = [-1] * graphe.n
        bellman_ford(graphe, distances, parent)
        if distances[graphe.g] == float('inf'):
            print("Aucun chemin améliorant disponible.")
            break
        cheminflot = desired_flow - current_flow
        v = graphe.g
        while v != graphe.source:
            u = parent[v]
            cheminflot = min(cheminflot, graphe.reste[u][v])
            v = u
        v = graphe.g
        while v != graphe.source:
            u = parent[v]
            graphe.reste[u][v] -= cheminflot
            graphe.reste[v][u] += cheminflot
            total_cost += graphe.cout[u][v] * cheminflot
            v = u
        current_flow += cheminflot
        print(f"Ajout de flot {cheminflot}, coût total = {total_cost}")
    graphe.Finalflot()
    print(f"\nFlot à coût minimal trouvé (valeur {current_flow}) avec coût total = {total_cost}")
    return total_cost
