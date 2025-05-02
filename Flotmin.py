class ReseauFlot:
    def __init__(self, capacites, couts, noms, val_flot):
        self.noms = noms
        self.n = len(noms)
        self.source = 0
        self.puits = self.n - 1
        self.val_flot = val_flot
        self.capacites = [row[:] for row in capacites]
        self.couts = [row[:] for row in couts]
        self.residuel = [row[:] for row in capacites]
        self.couts_residuel = [row[:] for row in couts]
        self.flot_total = 0
        self.cout_total = 0

    def bellman_ford(self):
        distances = [float('inf')] * self.n
        parents = [-1] * self.n
        distances[self.source] = 0

        for _ in range(self.n - 1):
            for u in range(self.n):
                for v in range(self.n):
                    if self.residuel[u][v] > 0 and distances[u] + self.couts_residuel[u][v] < distances[v]:
                        distances[v] = distances[u] + self.couts_residuel[u][v]
                        parents[v] = u
        return distances, parents

    def trouver_chemin(self, parents):
        chemin = []
        v = self.puits
        while v != self.source:
            u = parents[v]
            if u == -1:
                return []
            chemin.append((u, v))
            v = u
        chemin.reverse()
        return chemin

    def appliquer_chemin(self, chemin):
        flot_possible = min(self.residuel[u][v] for u, v in chemin)
        flot_envoye = min(flot_possible, self.val_flot - self.flot_total)
        cout_chemin = sum(self.couts_residuel[u][v] for u, v in chemin)

        for u, v in chemin:
            self.residuel[u][v] -= flot_envoye
            self.residuel[v][u] += flot_envoye
            self.couts_residuel[v][u] = -self.couts_residuel[u][v]

        self.flot_total += flot_envoye
        self.cout_total += flot_envoye * cout_chemin

        print(f"\nNouveau chemin trouvé : {' -> '.join(self.noms[u] for u, _ in chemin)} -> {self.noms[chemin[-1][1]]}")
        print(f"Flot injecté : {flot_envoye}, Coût du chemin : {cout_chemin}")
        print(f"Flot cumulé : {self.flot_total} / {self.val_flot}, Coût cumulé : {self.cout_total}")

    def resoudre(self):
        print("\n--- algorithme de flot à coût minimal ---")
        while self.flot_total < self.val_flot:
            distances, parents = self.bellman_ford()
            if distances[self.puits] == float('inf'):
                print("Aucun chemin restant vers le puits")
                break
            chemin = self.trouver_chemin(parents)
            if not chemin:
                print("Chemin non valide")
                break
            self.appliquer_chemin(chemin)
        print("\n--- ALGORITHME TERMINÉ ---")
        print(f"Flot total transmis : {self.flot_total}")
        print(f"Coût total du flot : {self.cout_total}")