from ..libs import *

# TRIMMING
def trim(self, add_false_edges = False):
    """
        Removes unnecessary nodes from the network if it is connected, otherwise returns false
    """
    if nx.is_connected(self.G):
        self._remove_unneeded_nodes()
        #self._remove_unneeded_edges()
        self._trim_redundant()
        
        if add_false_edges:
            self._add_false_edges()
            #self._remove_unneeded_edges()
            self._remove_unneeded_nodes()
        
        return True
    else:
        print("Network not fully connected")
        return False
   
def _remove_unneeded_nodes(self):
    # identify key nodes
    nodes_to_keep = set()
    for a in self._true_shortest_paths():
        for u in a:
            nodes_to_keep.add(u)
    
    # remove unneeded nodes
    for u in list(self.nodes).copy():
        if u not in nodes_to_keep:
            self.G.remove_node(u)

def _remove_unneeded_edges(self):
    # identify key edges
    keep_edges = set()
    for paths in self._true_shortest_paths():
        if len(paths) == 0: continue
        for i in range(1, len(paths)):
            keep_edges.add((paths[i-1], paths[i]))

    # remove unneeded edges
    for u,v in self.G.edges:
        if (u,v) not in keep_edges and (v,u) not in keep_edges:
            self.G.remove_edge(u,v)
            
def _trim_redundant(self):
    """
        Removes false nodes with only two edges
    """
    for u in list(self.nodes).copy():
        if self.nodes[u]["true_node"]: continue
        elif len(self.G[u]) == 2: # redundant node - remove
            self._add_edge(*[a for a in self.G[u]])
            self.G.remove_node(u)

def _add_false_edges(self):
    """
        add edges between all neighbour nodes of false nodes
    """
    for u in self.nodes:
        if not self.nodes[u]["true_node"]: # true node
            for e in self._all_pairs(u):
                self._add_edge(*e)


def _true_shortest_paths(self):
    """
        Returns the shortest paths from the original node to true nodes
    """
    return [nx.shortest_path(self.G, source = self.init_id, target = u, weight = "weight") 
                            for u in self.nodes if self.nodes[u]["true_node"]]