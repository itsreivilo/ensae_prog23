import time, random, numpy, math

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


    def add_edge(self, node1, node2, power_min, dist=1): # Question 1#
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
# On regarde pour chacun des deux noeuds si ils sont déjà dans le graphes ou non, auquel cas on les ajoute, sinon on rajoute seulement l'arrête
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)

        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)
#On rajoute l'arrête à chaque noeud, la puissance associée et la distance
        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))
        self.nb_edges += 1


    def connected_components(self): # Question 2 #

        A = []  # A contiendra les listes de composantes connectées
        nodes_v = {node: False for node in self.nodes}  # Dictionnaire qui permet de savoir si l'on est déjà passé par un point

        def components(node): # Fonction qui visite les noeuds 
            L = [node]

            for i in self.graph[node]:
                k = i[0]

                if not nodes_v[k]:
                    nodes_v[k] = True
                    L += components(k)  # On rajoute aux noeud ces composants

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


    def get_path_with_power(self, src, dest, power): # Question 3 #
        (u, v) = (src, dest)  # u et v correspondent au trajet, en étant chacun un nombre correspondant à un noeud
        a = 0
        # On vérifie que les deux villes sont dans la même composante connexe (et donc que le trajet est réalisable), si ce n'est pas le cas on renvoit 'None'
        for i in Graph.connected_components_set(self):

            if u not in i or v not in i:
                a +=1

        if a == len(Graph.connected_components_set(self)):
            return None

        # On étudie maintenant tous les chemins

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

        return M # Complexité de O(E)


    def min_power(self, src, dest): # Question 6 #
        """
        Should return path, min_power.
        """
        # On procède à une dichotomie en commencant par les puisances de 2 afin d'éviter de tester trop de puissances
        i = 1
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

    # Pour la complexité : on utilise get_path_with_power dans l'algorithme dichotomique, la dichotomie se fait en O(log(i)), ici i est la puissance de 2 minimal qui dépasse p_min
    # La complexité est donc de O(E*i) = O(E).

def graph_from_file(filename): # Question 1 et 4 #
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
                g.add_edge(node1, node2, power_min) # Si la distance n'est pas précisée, la valeur par défaut est 1

            elif len(edge) == 4:
                node1, node2, power_min, dist = edge
                g.add_edge(node1, node2, power_min, dist)

            else:
                raise Exception("Format incorrect")

    return g


# Question 10 #
def fonction_chrono(filename,  g_ch): 

    t = time.perf_counter()
# Ouverture du fichier et récupération des données
    with open(filename, "r") as file:
        k = map(int, file.readline().split())
# On choisit au hasard un trajet et on applique la fonction, on repète le processus 100 fois pour trouver une valeur moyenne
    for i in range(100):
        a = g_ch.nodes[random.randint(0,len(g_ch.nodes)-1)]
        b = g_ch.nodes[random.randint(0,len(g_ch.nodes)-1)]
        M = g_ch.min_power(a,b)
        L, p = M[0], M[1]

    t_int = time.perf_counter()
    t_fin = (t_int - t)*(k/100)
    return t_fin

# Test de la fonction et du temps nécessaire (semble ne pas fonctionner pour le moment mais nous n'avons pas encore réussi à résoudre ce problème)
for x in range(1,11):
    L= []
    g_ch = graph_from_file('input/network.'+str(x)+'.in')
    route = 'input/routes.'+str(x)+'.in'
    L.append(fonction_chrono(route,g_ch))
print(L)


# Question 12 #
def kruskal(g):
    A = []
    L = [] # L correspondra à l'arbre couvrant minimal, avec les noeuds du haut vers le bas

    for a in g.connected_components(): # On applique ce processus à chaque composante connexe
        R = []  # R sera la liste des arrêtes de chacune des composantes connexes
        T = []

        for i in range(len(a)):
            b = a[i]
            T.append([])

            for j in g.graph[b]:

                if j not in(R):
                    T[i].append((a[i], j[0], j[1]))
                    R.append(j)

        for i in T:
            A += i   # Maintenant on a la liste des arrêtes sous la forme (noeud1,noeud2,puissance), ce qui va nous servir pour l'Union-Find 

        N = len(R)

        for n in range(1,N): # On trie les arrêtes par ordre croissant
            cle = R[n]
            j = n-1

            while j>=0 and R[j][2] > cle[2]:
                R[j+1] = R[j]
                j = j-1

            R[j+1] = cle

        # On va maintenant se servir de l'Union-Find pour déterminer si l'arrête ajoutée crée un cycle ou pas 

        Parent = {x: None for x in g.nodes}
        
        def Find(x):

            if Parent[x] == None:
                Parent[x] = x
                return x

            else:
                return Find(Parent[x])


        def Union(x,y):
            xracine = Find(x)
            yracine = Find(y)

            if xracine != yracine:
                Parent[xracine] = [yracine]
        

        for a in R:
            u, v = a[0], a[1]

            if Find(u) != Find(v):
                L.append(a)
                Union(u,v)

    return L, Parent
# Nous rencontrons encore des difficultés à terminer l'Union-Find de façon fonctionnelle

# Question 13 #

g = graph_from_file('input/network.01.in')
print(kruskal(g))

# Question 14 # 

def min_power_opti(g,t):

    A, Parent = kruskal(g)

    # On a la liste des arrêtes et en se servant du dictionnaire on connait l'ordre des noeuds 

    (source, destination) = t
    M = [source]
    N = [destination]
    return min_power(g, source, destination)


# Question 15

# N'ayant pas, pour le moment, réussi à faire fonctionner notre fonction test pour la Q10, nous ne pouvons pas encore comparer ces résultats