import numpy as np

class Graph:
    def __init__(self, filename):
        self.GrapheFichier(filename)

    def GrapheFichier(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()

        if len(lines) == 1 + 2 * int(lines[0].strip()):
            self.problem_type = 'cout_min'
        else:
            self.problem_type = 'flot_max'

        self.n = int(lines[0].strip())
        self.c = np.zeros((self.n, self.n), dtype=int)
        self.cout = np.zeros((self.n, self.n), dtype=int)

        for i in range(1, self.n + 1):
            row = list(map(int, lines[i].strip().split()))
            self.c[i - 1] = row

        if self.problem_type == 'cout_min':
            for i in range(self.n + 1, 2 * self.n + 1):
                row = list(map(int, lines[i].strip().split()))
                self.cout[i - self.n - 1] = row

        self.source = 0
        self.g = self.n - 1
        self.flot = np.zeros((self.n, self.n), dtype=int)
        self.reste = np.copy(self.c)

    def AfficherMatrice(self, matrice):
        noms = ['s'] + [chr(ord('a') + i) for i in range(0, self.n - 2)] + ['t']
        temp = max(len(str(matrice[i][j])) for i in range(self.n) for j in range(self.n)) + 3

        # En-tête des colonnes
        en_tete = " " * (temp + 1) + "".join(n.center(temp) for n in noms)
        print(en_tete)

        # Corps de la matrice avec noms de lignes
        for i in range(self.n):
            ligne = noms[i].ljust(temp + 1)
            ligne += "".join(str(matrice[i][j]).center(temp) for j in range(self.n))
            print(ligne)

    def noms_sommets(self):
        return ['s'] + [chr(ord('a') + i) for i in range(0, self.n - 2)] + ['t']



    def print_matrices(self):
        print("\nMatrice des capacités :")
        self.AfficherMatrice(self.c)
        if self.problem_type == 'cout_min':
            print("\nMatrice des coûts :")
            self.AfficherMatrice(self.cout)

    def AfficherFlot(self):
        print("\nFlot final :")
        self.AfficherMatrice(self.flot)

    def Finalflot(self):
        matrice_flot = [[""] * self.n for _ in range(self.n)]

        for i in range(self.n):
            for j in range(self.n):
                if self.c[i][j] > 0:
                    flot_ij = self.c[i][j] - self.reste[i][j]
                    matrice_flot[i][j] = f"{flot_ij}/{self.c[i][j]}"
                else:
                    matrice_flot[i][j] = "0"

        print("\nFlot final (format flot/capacité) :")
        self.AfficherMatrice(matrice_flot)
