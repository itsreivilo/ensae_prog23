import numpy
import math

class Graph:
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output

    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes.

        Parameters:
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        nodes = self.nodes
        i = 0
        if node1 not in nodes:
            nodes.append(node1)
            self.graph[node1] = [(node2, power_min, dist)]
            i += 1
        else:
            self.graph[node1].append((node2, power_min, dist))

        if node2 not in nodes:
            nodes.append(node2)
            self.graph[node2] = [(node1, power_min, dist)]
            i += 1
        else:
            self.graph[node2].append((node1, power_min, dist))

        self.nodes = nodes
        self.nb_nodes += i
        self.nb_edges += 1

    def get_path_with_power(self, p, t):
        (u, v) = t  # u et v sont deux chiffres qui representent un noeud
        a = 0
        # Si les deux villes u et v ne sont pas dans une même composante connexe on renvoit 'None'
        for i in Graph.connected_components_set(self):
            if u not in i or v not in i:
                a +=1
        if a == len(Graph.connected_components_set(self)):
            return None

        # Donc les deux villes sont dans une même composante, maintenant on va étudier tous les chemins
        precedent = {x: None for u in self.nodes}
        Deja_traite = {x: False for u in self.nodes}
        distance = {x: float('inf') for x in self.nodes}
        distance[u] = 0
        A_traiter = [(distance[u], u)]
        while A_traiter:
            dist_noeud, noeud = A_traiter.pop()
            if not Deja_traite(noeud):
                Deja_traite[noeud] = True
                for (voisin, p_min, d) in self.graph[noeud]:
                    dist_voisin = dist_noeud + d
                    if p >= p_min and dist_voisin < distance[voisin]:
                        distance[voisin] = dist_voisin
                        precedent[voisin] = noeud
                        A_traiter.append((dist_voisin, voisin))
            A_traiter.sort(reverse=True)
        l = len(precedent)
        L = [v]
        b = 0  # distance
        a = precedent(v)
        for i in range(len(precedent)):
            L.append(a)
            b += distance[a]
            if a == u:
                break
            a = precedent(a)
        return (L, b)

    def connected_components(self):
        A = []  # listes vides qui contiendra les listes de composants connectés
        nodes_v = {node: False for node in self.nodes}  # dictionnaire qui permet de savoir si l'on est déjà passé par un point

        def components(node):
            L = [node]
            for i in self.graph[node]:
                k = i[0]
                if not nodes_v[k]:
                    nodes_v[k] = True
                    L += components(k)  # on rajoute aux noeud ces composants
            return L

        for k in self.nodes:
            if not nodes_v[k]:
                A.append(components(k))

        return A

    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component),
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))

    def min_power(self, src, dest):
        """
        Should return path, min_power.
        """
        t = (src, dest)
        j = 0
        i = 2**j
        g = Graph.get_path_with_power(self, i, t)

        while g is None:
            j += 1
            g = Graph.get_path_with_power(self, i, t)

        bas = 2**(j-1)
        haut = i

        while abs(bas-haut) > 1:
            milieu = math.floor((haut+bas)/2)
            h = Graph.get_path_with_power(self, milieu, t)
            if h is None:
                bas = milieu
            else:
                haut = milieu

        return (math.floor(milieu), h[0])

    def graph_from_file(filename):
        """
        Reads a text file and returns the graph as an object of the Graph class.

        The file should have the following format:
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.
        Parameters:
        -----------
        filename: str
        The name of the file
        Outputs:
        -----------
        G: Graph
        An object of the class Graph with the graph from file_name.
        """

        g = Graph()
        fichier = open(filename, "r")
        fichier1 = fichier.readlines()
        L = fichier1[0].split()
        (n, m) = (int(L[0]), int(L[1]))
        for i in range(1, m+1):
            A = fichier1[i].split()
            if len(A) == 4:
                g.add_edge(int(A[0]), int(A[1]), int(A[2]), int(A[3]))
            else:
                g.add_edge(int(A[0]), int(A[1]), int(A[2]), 1)
        fichier.close()
        return g


# pour appeler un fichier, '..\nomdufichier' les deux points representent un retour en arrière
# g = graph_from_file('/home/onyxia/ensae_prog23/input/network.00.in')
# print(g)



g = Graph.graph_from_file('/home/onyxia/work/ensae_prog23/input/network.01.in')
print(g)

print(len(g.connected_components_set()))
