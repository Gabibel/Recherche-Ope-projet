from collections import deque

def bfs(graphe, parent):
    visite = [False] * graphe.n
    queue = deque([graphe.source])
    visite[graphe.source] = True
    parent[graphe.source] = -1
    while queue:
        u = queue.popleft()
        for v in range(graphe.n):
            if not visite[v] and graphe.reste[u][v] > 0:
                queue.append(v)
                visite[v] = True
                parent[v] = u
                if v == graphe.g:
                    return True
    return False

def ford_fulkerson(graphe):
    parent = [-1] * graphe.n
    flotmax = 0
    ite = 1
    print("\nDébut de l'algorithme Ford-Fulkerson")
    while bfs(graphe, parent):
        print(f"\n⋆ Itération {ite}:")
        graphe.AfficherParents(parent)
        cheminflot = float("inf")
        s = graphe.g
        chemin = []
        while s != graphe.source:
            chemin.append(s)
            cheminflot = min(cheminflot, graphe.reste[parent[s]][s])
            s = parent[s]
        chemin.append(graphe.source)
        chemin.reverse()
        noms = graphe.noms_sommets()
        print("Chaîne améliorante trouvée:", " → ".join([noms[p] for p in chemin]), f"de flot {cheminflot}")

        v = graphe.g
        while v != graphe.source:
            u = parent[v]
            graphe.reste[u][v] -= cheminflot
            graphe.reste[v][u] += cheminflot
            v = parent[v]
        print("Matrice résiduelle après modification :")
        graphe.AfficherMatrice(graphe.reste)
        flotmax += cheminflot
        ite += 1
    print(f"\nFlot maximal trouvé: {flotmax}")
    return flotmax

def push_relabel(graphe):
    print("\nDébut de l'algorithme Pousser-Réétiqueter")
    graphe.reste = graphe.c - graphe.flot
    h = [0] * graph.n
    e = [0] * graph.n
    h[graphe.source] = graphe.n
    for v in range(graphe.n):
        if graphe.c[graph.source][v] > 0:
            graphe.flot[graphe.source][v] = graphe.c[graphe.source][v]
            graphe.flot[v][graphe.source] = -graphe.flot[graphe.source][v]
            e[v] = graphe.flot[graph.source][v]
            e[graphe.source] -= graphe.flot[graphe.source][v]
    active = [i for i in range(graphe.n) if i != graphe.source and i != graphe.g and e[i] > 0]
    while active:
        u = active[0]
        temp2 = False
        for v in range(graphe.n):
            if graphe.reste[u][v] > 0 and h[u] == h[v] + 1:
                delta = min(e[u], graphe.reste[u][v])
                graphe.reste[u][v] -= delta
                graph.reste[v][u] += delta
                e[u] -= delta
                e[v] += delta
                print(f"Poussée de {delta} de v{u+1} vers v{v+1}")
                if v != graphe.source and v != graphe.g and v not in active and e[v] > 0:
                    active.append(v)
                if e[u] == 0:
                    break
                temp2 = True
        if not temp2:
            min_h = min([h[v] for v in range(graphe.n) if graphe.reste[u][v] > 0], default=float('inf'))
            h[u] = min_h + 1
            print(f"Réétiquetage de v{u+1} à hauteur {h[u]}")
        if e[u] == 0:
            active.pop(0)
    graphe.Finalflot()
    flotmax = sum(graphe.flot[graphe.source][i] for i in range(graphe.n))
    print(f"\nFlot maximal trouvé: {flotmax}")
    return flotmax
