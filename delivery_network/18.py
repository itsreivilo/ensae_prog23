#Question 18
from graph import Graph, graph_from_file
from operator import itemgetter
#Première idée : algorithme glouton

# On commence par associer à chaque trajet le profit rapporté 
j = graph_from_file('network.1.in')

g = open('routes.1.in', 'r')
L = []
n = g.readline()

for _ in range(n):
    edge = list(map(int, g.readline().split()))
    src, dst, util = edge
    L.append(((src,dst),util))
    if len(edge) != 3:
        raise Exception("Format incorrect")

# L est la liste des trajets et de l'utilité associée


h = open('trucks.1.in', 'r')
C = []
m = h.readline()

for _ in range(m):
    edge = list(map(int, h.readline().split()))
    power, cout = edge
    L.append((power, cout))
    if len(edge) != 2:
        raise Exception("Format incorrect")

# C est la liste des coûts et de la puissance

'''for each trajet 
on cherche la puissance min necessaire
on cherche le camion le moins cher avce au moins cette puissance et on lajoute
on se retrouvera avec une liste de tuples (trajet, utilite, cout)
profit = utilite - cout
liste de tuples (trajet, utilite, cout, profit)'''

L_Sort = sorted(L, key=itemgetter(1), reverse=True)
# On trie les trajets par ordre décroissant de profit

C_Sort = sorted(C, key=itemgetter(0,1))
# On trie les camions par ordre croissant de puissance puis par ordre croissant de coût

B = 25*(10**9)
# B est le budget de l'entreprise

R = []
# R sera la liste des camions à acheter associés à leur trajet respectif

Pi = 0
# Pi sera le profit total

for i in range(len(L_Sort)) :
    puis = Graph.min_power(self, L_Sort[i][0])
    J = []
    while J == []:
        for j in range(len(C_Sort)):
            if C_Sort[j][0] >= puis:
                J.append(C_Sort[j][0])
    if J[0][1] <= B:
        B = B - J[0][1]
        R.append((L_Sort[i][0], C_Sort[j]))
        Pi += J[0][0]

print('La liste des camions à acheter est : ', R,'\n Le profit total ainsi réalisé par l\'entreprise sera de', Pi, 'et son budget restant sera de', B)
