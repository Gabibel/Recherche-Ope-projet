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

def afficher_parcours_largeur(graphe, parent):
    niveaux = {}
    noms = graphe.noms_sommets()

    for v in range(graphe.n):
        if parent[v] != -1: 
            niveau = 0
            u = v
            while parent[u] != -1:
                niveau += 1
                u = parent[u]
            if niveau not in niveaux:
                niveaux[niveau] = []
            niveaux[niveau].append(v)

    
    print("Parcours en largeur :")
    print(f"s :")
    for niveau in sorted(niveaux.keys()):
        ligne = "".join(
            [noms[v] if v != 0 and v != graphe.n-1 else ('s' if v == 0 else 't') 
             for v in niveaux[niveau]]
        )
        
        parents = " , ".join(
            [f"Π({noms[v]}) = {noms[parent[v]]}" if v != 0 and v != graphe.n-1 
             else (f"Π({('s' if v == 0 else 't')}) = {'-' if parent[v] == -1 else noms[parent[v]]}")
             for v in niveaux[niveau]]
        )
        
        print(f"{ligne} : {parents}")

    if graphe.n-1 in parent and parent[graphe.n-1] != -1:
        print(f"t : Π(t) = {noms[parent[graphe.n-1]]}")


def ford_fulkerson(graphe):
    parent = [-1] * graphe.n
    flotmax = 0
    ite = 1
    print("\nDébut de l'algorithme Ford-Fulkerson")
    while bfs(graphe, parent):
        print(f"\n⋆ Itération {ite}:")
        afficher_parcours_largeur(graphe, parent)

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
    n = graphe.n
    s = graphe.source
    t = graphe.g

    # Initialisation
    graphe.reste = graphe.c - graphe.flot
    h = [0] * n
    e = [0] * n
    h[s] = n

    # Pré-flux depuis la source
    for v in range(n):
        if graphe.c[s][v] > 0:
            flow = graphe.c[s][v]
            graphe.flot[s][v] = flow
            graphe.flot[v][s] = -flow
            graphe.reste[s][v] -= flow
            graphe.reste[v][s] += flow
            e[v] = flow
            e[s] -= flow

    active = [i for i in range(n) if i != s and i != t and e[i] > 0]

    while active:
        u = active[0]
        pushed = False
        for v in range(n):
            if graphe.reste[u][v] > 0 and h[u] == h[v] + 1:
                delta = min(e[u], graphe.reste[u][v])
                graphe.flot[u][v] += delta
                graphe.flot[v][u] -= delta
                graphe.reste[u][v] -= delta
                graphe.reste[v][u] += delta
                e[u] -= delta
                e[v] += delta
                print(f"Poussée de {delta} de v{u+1} vers v{v+1}")
                if v != s and v != t and v not in active and e[v] > 0:
                    active.append(v)
                if e[u] == 0:
                    break
                pushed = True
        if not pushed:
            min_h = min([h[v] for v in range(n) if graphe.reste[u][v] > 0], default=float('inf'))
            h[u] = min_h + 1
            print(f"Réétiquetage de v{u+1} à hauteur {h[u]}")
        if e[u] == 0:
            active.pop(0)

    graphe.Finalflot()
    flotmax = sum(graphe.flot[s][i] for i in range(n))
    print(f"\nFlot maximal trouvé: {flotmax}")
    return flotmax
