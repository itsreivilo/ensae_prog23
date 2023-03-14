import numpy
import math

class Graph:
    
    """
    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented. 
    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...]
        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 
        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
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

        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1


    def get_path_with_power(self, src, dest, power):
        (u, v) = (src, dest)  # u et v sont deux chiffres qui representent un noeud
        a = 0
        # Si les deux villes u et v ne sont pas dans une même composante connexe on renvoit 'None'
        for i in Graph.connected_components_set(self):
            if u not in i or v not in i:
                a +=1
        if a == len(Graph.connected_components_set(self)):
            return None

        # Donc les deux villes sont dans une même composante, maintenant on va étudier tous les chemins
        precedent = {x: None for x in self.nodes}

        Deja_traite = {x: False for x in self.nodes}

        distance = {x: float('inf') for x in self.nodes}

        distance[u] = 0

        A_traiter = [(distance[u], u)]

        while A_traiter:

            dist_noeud, noeud = A_traiter.pop()

            if not Deja_traite[noeud]:

                Deja_traite[noeud] = True

                for (voisin, p_min, d) in self.graph[noeud]:

                    dist_voisin = dist_noeud + d

                    if power >= p_min:

                        if dist_voisin < distance[voisin]:

                            distance[voisin] = dist_voisin

                            precedent[voisin] = noeud

                            A_traiter.append((dist_voisin, voisin))



            A_traiter.sort(reverse=True)
        l = len(precedent)
        L = [v]
        a = precedent[v]

        for i in range(len(precedent)):

            L.append(a)

            if a == u:

                break

            if a == None:

                return None

            a = precedent[a]

        M = []

        for i in range(len(L)):
            M.append(L[-i-1])
        return M


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

        j = 0

        i = 2**j

        g = Graph.get_path_with_power(self, src, dest, i)

        while g is None:
            i *= 2
            g = Graph.get_path_with_power(self, src, dest, i)


        bas = i/2
        haut = i

        while abs(bas-haut) > 1:

            milieu = math.floor((haut+bas)/2)

            h = Graph.get_path_with_power(self, src, dest, milieu)

            if h is None:

                bas = milieu

            else:

                haut = milieu


        return [h, math.floor(haut)]


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
    g: Graph
        An object of the class Graph with the graph from file_name.
    """

    with open(filename, "r") as file:
        n, m = map(int, file.readline().split())

        g = Graph(range(1, n+1))

        for _ in range(m):

            edge = list(map(int, file.readline().split()))

            if len(edge) == 3:

                node1, node2, power_min = edge

                g.add_edge(node1, node2, power_min) # will add dist=1 by default

            elif len(edge) == 4:

                node1, node2, power_min, dist = edge

                g.add_edge(node1, node2, power_min, dist)

            else:

                raise Exception("Format incorrect")

    return g


import time, random




def fonction_chrono(filename,  g_ch): # Question 10, chronométrer le temps pris par la fonction min power pour chacun des fichiers routes.x.input #


    t = time.perf_counter()

    with open(filename, "r") as file:
        k = map(int, file.readline().split())

    for i in range(100):

        a = g_ch.nodes[random.randint(0,len(g_ch.nodes)-1)]

        b = g_ch.nodes[random.randint(0,len(g_ch.nodes)-1)]

        M = g_ch.min_power(a,b)

        L, p = M[0], M[1]

    t_int = time.perf_counter()




    t_fin = (t_int - t)*(k/100)

    return t_fin


for x in range(1,11):

    L= []
    g_ch = graph_from_file('input/network.'+str(x)+'.in')
    route = 'input/routes.'+str(x)+'.in'

    L.append(fonction_chrono(route,g_ch))

print(L)

# Fin de la question 10 #



# Question 12 #



def kruskal(g):
    L = [] # l'arbre couvrant minimal du haut vers le bas des noeuds #

    for a in g.connected_components(): # j'applique kruskal sur chaque composante connexe de g #

        R = []  # liste des arrêtes de a ( la composante connexe) # 

        T = []

        for i in a:

            T.append([])

            for j in g.graph[i]:

                if j not in(R):

                    T[i].append((i,j(0),j(1)))

                    R.append(j)

        for i in T:

            A += i   # Maintenant on a la liste des arrêtes sous la forme (noeud1,noeud2,puissance), ce qui va nous servir pour l'Union-Find #

        N = len(R)

        for n in range(1,N): # on applique un tri par insertion sur les puissances des arrêtes #

            cle = R[n]

            j = n-1

            while j>=0 and R[j](2) > cle(2):

                R[j+1] = R[j]

                j = j-1

            R[j+1] = cle

        # On va maintenant se servir de l'Union-Find pour déterminer si l'arrete ajouter créer un cycle ou pas #

        Parent = {x for x in g.nodes}

        def Find(x):

            if Parent[x] == []:

                Parent[x].append(x)

                return x

            else:

                return Find(Parent[x][0])

        def Union(x,y):

            xracine = Find(x)

            yracine = Find(y)

            if xracine != yracine:

                Parent[xracine] = [yracine]

        for a in R:

            u, v = a(0), a(1)

            if Find(u) != Find(v):

                L.append(a)

                Union(u,v)

    return L, Parent



# Question 14 # 



def min_power_opti(g,t):

    A, Parent = kruskal(g)

    # On a la liste des arrêtes et en se servant du dictionnaire on connait l'ordre des noeuds #

    (source, destination) = t

    M = [source]

    N = [destination]

    return min_power(g, source, destination)



fonction_chrono(filename)