#Question 18
from graph import Graph, graph_from_file
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

#C est la liste des coûts et de la puissance

'''for each trajet 
on cherche la puissance min necessaire
on cherche le camion le moins cher avce au moins cette puissance et on lajoute
on se retrouvera avec une liste de tuples (trajet, utilite, cout)
profit = utilite - cout
liste de tuples (trajet, utilite, cout, profit)'''

sort les trajets par utilite descending

for each trajet tries 
pour le premier on regarde puissance minimale necessaire
camion le moins cher qui a au moins cette puissance
si son cout plus petit que le budget restsnat 
on achete  et on l attribue a ce trajet 
sinon on le prend pas et on passe au suivant 

return la liste des (camions associes au trajet) et le budget restant et la somme du profit?
