def afficher_table_bellman_etendue(noms, etapes, residuel):
    print("\n╔══════════════════════════════════════════════╗")
    print("║        Table d'évolution Bellman-Ford        ║")
    print("╚══════════════════════════════════════════════╝")

    headers = ["Étape"] + noms
    largeur = 10
    print(" | ".join(f"{h:^{largeur}}" for h in headers))
    print("-" * ((largeur + 3) * len(headers) - 1))

    n = len(noms)
    for k in range(len(etapes) + 1):
        ligne = [f"{k:^10}"]
        if k == 0:
            ligne += [f"{'0':^10}"] + [f"{'+∞':^10}"] * (n - 1)
        else:
            distances, parents = etapes[k - 1]
            for i in range(n):
                if distances[i] == float('inf'):
                    ligne.append(f"{'+∞':^10}")
                elif parents[i] == -1:
                    ligne.append(f"{distances[i]:^10}")
                else:
                    ligne.append(f"{distances[i]}({noms[parents[i]]})".center(10))
        print(" | ".join(ligne))
    print("-" * ((largeur + 3) * len(headers) - 1))

    print("\nCapacité totale sortante de s :", sum(residuel[0]))
    print("Capacité totale entrante dans t :", sum(residuel[i][-1] for i in range(n)))
    print("Flot maximum envoyable :", min(
        sum(residuel[0]), sum(residuel[i][-1] for i in range(n))
    ))


class ReseauFlot:
    def __init__(self, capacites, couts, noms, val_flot):
        self.noms = noms
        self.n = len(noms)
        self.source = 0
        self.puits = self.n - 1
        self.val_flot = val_flot
        self.residuel = [row[:] for row in capacites]
        self.couts_residuel = [row[:] for row in couts]
        self.flot_total = 0
        self.cout_total = 0

    def afficher_matrice_residuelle(self):
        print("\n--- Graphe résiduel (capacités ; coûts) ---")
        print(" " * 8 + " | ".join(f"{nom:^8}" for nom in self.noms))
        print("-" * (10 + 11 * self.n))
        for i in range(self.n):
            ligne = f"{self.noms[i]:<8}| "
            for j in range(self.n):
                if self.residuel[i][j] > 0:
                    val = f"{self.residuel[i][j]}|{self.couts_residuel[i][j]}"
                else:
                    val = "0"
                ligne += f"{val:^8}| "
            print(ligne)

    def bellman_ford(self):
        distances = [float('inf')] * self.n
        parents = [-1] * self.n
        distances[self.source] = 0

        etapes = []

        for it in range(1, self.n):
            changed = False
            new_distances = distances[:]
            new_parents = parents[:]
            for u in range(self.n):
                for v in range(self.n):
                    if self.residuel[u][v] > 0 and distances[u] + self.couts_residuel[u][v] < new_distances[v]:
                        new_distances[v] = distances[u] + self.couts_residuel[u][v]
                        new_parents[v] = u
                        changed = True
            etapes.append((new_distances[:], new_parents[:]))
            if not changed:
                break
            distances = new_distances
            parents = new_parents

        afficher_table_bellman_etendue(self.noms, etapes, self.residuel)
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

        print(f"\nChemin trouvé : {' -> '.join(self.noms[u] for u, _ in chemin)} -> {self.noms[chemin[-1][1]]}")
        print(f" Flot evnoyé : {flot_envoye}, Coût : {cout_chemin}")
        print(f" Flot cumulé : {self.flot_total} / {self.val_flot}, Coût cumulé : {self.cout_total}")

        self.afficher_matrice_residuelle()

    def resoudre(self):
        print("\nalgorithme de flot à coût minimal (Bellman-Ford)\n")
        while self.flot_total < self.val_flot:
            distances, parents = self.bellman_ford()
            if distances[self.puits] == float('inf'):
                print("Aucun chemin disponible.")
                break
            chemin = self.trouver_chemin(parents)
            if not chemin:
                print("Pas de chemin valide.")
                break
            self.appliquer_chemin(chemin)
        print("\n----------------------")
        print(f"Flot total : {self.flot_total}")
        print(f"Coût total : {self.cout_total}")