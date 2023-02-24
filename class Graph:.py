import numpy


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

    def get_path_with_power(self, src, dest, power):
        raise NotImplementedError

    def connected_components(self):
        A=[] #listes vides qui contiendra les listes de composants connectés
        nodes_v={node : False for node in self.nodes} #dictionnaire qui permet de savoir si l'on est déjà passé par un point

        def components(node) :
            L=[node]
            for i in self.graph[node] :
                k=i[0]
                if not nodes_v[k] :
                    nodes_v[k]=True
                    L+=components(k) #on rajoute aux noeud ces composants
            return L
        
        for k in self.nodes :
            if not nodes_v[k] : A.append(components(k))

        return A

""" # On définit les matrices d'adjacences
        n = self.nb_nodes
        M = [[0 for i in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if self.nodes[j] in self.graph[self.nodes[i]]:
                    M[i][j] = 1
                    M[j][i] = 1
        for i in range(n):
            M[i][i] = 1

        T = numpy.arange(n)

        modifications = True
        while modifications:
            modifications = False
            for i in range(n):
                for j in range(i+1, n):
                    if M[i, j] == 1 and T[i] != T[j]:
                        T[i] = T[j] = min(T[i], T[j])
                        modifications = True
        cnx = T
        res = {}
        for i, c in enumerate(cnx):
            if c not in res:
                res[c] = []
            res[c].append(i)
        return res
"""
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
        raise NotImplementedError


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


""" ce qu'il a ecrit au tableau
get_component(G,v)
composantes connexes de v

def visited (u) :
    for i in 
    pour u dans V
true si u dans C(v)
false sinon

def explore (G,v):
    visited[v]=true
    for each (u,v) dans E :
        if not visited(u):
            explore(u)


DFS
for all v dans V
visited = false
for all v dans V
if not visited(v):
    explore(v)
 
 
 
 faire un test
cdFolder rentrer dans le fichier
ls pour voir les fichiers dans le fichier

 """