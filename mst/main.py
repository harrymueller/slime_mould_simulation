import networkx as nx

from haversine import calculate_distance
from networkx.algorithms.tree import minimum_spanning_tree

class MST():
    from slime.methods.displaying import plot
    
    def __init__(self, init_graph, init_id):
        """
            Initialise the network based on the graph given. 
        """
        self.G = nx.Graph() # init graph
        self.nodes = self.G.nodes # shortcut for getting nodes
        self.init_id = init_id

        # add all real nodes
        for (i, g_id) in enumerate(init_graph.nodes()):
            self.G.add_node(i+1 if g_id != init_id else 0, # id of root node is 0
                            latitude = init_graph.nodes[g_id]["latitude"], 
                            longitude = init_graph.nodes[g_id]["longitude"],
                            true_node = True)
            
    def _all_pairs(self):
        """
            Generates all pairs of nodes. From ThinkComplexity - Chp3
        """
        for i, u in enumerate(self.nodes):
            for j, v in enumerate(self.nodes):
                if i < j:
                    yield u, v

    def add_all_edges(self, R = 6371, use_eucl = False):
        for (u,v) in self._all_pairs():
            self.G.add_edge(u,v,weight = calculate_distance(self.nodes[u], self.nodes[v], R = R, use_eucl = use_eucl))
            
    def apply_mst(self, algorithm = "prim"):
        self.G = minimum_spanning_tree(self.G, algorithm = algorithm)