# Question 8 : Tests sur les algorithmes fournis #

from graph import Graph, graph_from_file, kruskal, fonction_chrono, fonction_chrono_opti




data_path = "input/"
file_name = "network.04.in"

g = graph_from_file(data_path + file_name)
# print(g)

# print(Graph.connected_components(g))

# print(Graph.get_path_with_power(g, 1, 3, 50))

print(Graph.min_power(g, 1, 4))

# Test de la fonction et du temps nécessaire Q10
def temps_chemin(x):
    g_ch = graph_from_file('input/network.'+str(x)+'.in')
    route = 'input/routes.'+str(x)+'.in'
    print(fonction_chrono(route,g_ch))
    


# Question 13 #
"""
g = graph_from_file('input/network.04.in')
print(kruskal(g))
"""
# Question 15 #


def temps_chemin_opti(x):
    g_ch = graph_from_file('input/network.'+str(x)+'.in')
    route = 'input/routes.'+str(x)+'.in'
    print(fonction_chrono_opti(route,g_ch))

print(temps_chemin_opti(1))
