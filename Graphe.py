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
        n = self.n
        temp = max(len(str(matrice[i][j])) for i in range(n) for j in range(n)) + 3
        matrice2 = " " * (temp + 1) + "".join(f"v{j+1}".center(temp) for j in range(n))
        print(matrice2)
        for i in range(n):
            row = f"v{i+1}".ljust(temp + 1)
            row += "".join(str(matrice[i][j]).center(temp) for j in range(n))
            print(row)

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
        for i in range(self.n):
            for j in range(self.n):
                if self.c[i][j] > 0:
                    self.flot[i][j] = self.c[i][j] - self.reste[i][j]
