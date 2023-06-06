import math
from haversine import calculate_distance

# from chap03
def _all_pairs(self, n = None):
    """Generates all pairs of nodes."""
    nodes = self.nodes if n is None else self.G[n]
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if i < j:
                yield u, v
                
def _calc_dist_nodes(self, pos1, pos2):
    """
        Wrapper around calculate_distance.py
        Calculates the distance between pos1 and pos2. Uses euclidean if `eucl`, haversine otherwise
    """
    return calculate_distance(pos1, pos2, self.conf.R, self.conf.use_eucl)

def _connect_all(self):
    """
        Connects all nodes within SEEING DIST
    """
    for (u,v) in self._all_pairs():
        if self._calc_dist_nodes(self.nodes[u], self.nodes[v]) < self.conf.seeing_dist:
            self._add_edge(u,v)

def _add_edge(self, u: int, v: int, ll = None):
    """
        Adds an weighted edge to the graph between u and v - optional dict of ll to use instead of u
    """
    self.G.add_edge(u, v, weight = self._calc_dist_nodes(self.nodes[u] if ll is None else ll, self.nodes[v]))

