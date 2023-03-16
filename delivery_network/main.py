# Question 8 : Tests sur les algorithmes fournis #

from graph import Graph, graph_from_file


data_path = "input/"
file_name = "network.04.in"

g = graph_from_file(data_path + file_name)
# print(g)

# print(Graph.connected_components(g))

# print(Graph.get_path_with_power(g, 1, 3, 50))

print(Graph.min_power(g, 1, 4))
