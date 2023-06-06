import networkx as nx
from copy import deepcopy
import matplotlib as mpl
import numpy as np

def _construct_graph(self):
    """
        Constructs the graph
    """
    # create graph
    self.G = nx.from_pandas_edgelist(self.data.connections, "station1", "station2", "weight")
    
    # add node attributes
    stations_dict = self.data.stations.drop("id", axis=1).to_dict("index")
    nx.set_node_attributes(self.G, stations_dict)

def plot(self, colour_by_zone = False, node_size = 15, filename = None):
    """
        Display the graph
    """
    # center station in blue
    if colour_by_zone: 
        zones = np.unique(self.data.stations.zone)
        cmap = mpl.cm.get_cmap('viridis')

        colour_dict = {}
        for (i,z) in enumerate(zones):
            # get rgba
            rgba = cmap(i/(len(zones)-1))
            # get hex codes
            hex = "#{:2X}{:2X}{:2X}".format(*[int(a*255) for a in rgba[:-1]])
            colour_dict[z] = hex.replace(" ", "0")
        colours = [colour_dict[self.G.nodes[i]["zone"]] for i in self.G.nodes]
    else: colours = ["tab:blue" if i == self.init["id"] else "tab:green" for i in self.G.nodes]

    # draw
    nx.draw(self.G, self.data.positions,
            node_color=colours, 
            node_shape='.', 
            node_size=node_size, 
            with_labels=False)

    if filename: mpl.pyplot.savefig(filename, dpi = 750, bbox_inches='tight')
            
def get_graph(self, with_edges = False):
    """
        Returns a NetworkX graph
    """
    if with_edges: return deepcopy(self.G)
    else: 
        G = nx.Graph()
        G.add_nodes_from(self.G.nodes(data = True))
        return G