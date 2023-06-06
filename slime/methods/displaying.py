from ..libs import *

# DISPLAYING
def plot(self):
    """
        Create a plot of the graph, with nodes in correct lat/lon positions.
        The initial node is red, true nodes are blue, and growth nodes are blue.
    """
    # get positions and colours
    pos = [(self.nodes[i]["longitude"], self.nodes[i]["latitude"]) 
                if i in (self.G.nodes()) else (0,0) 
                for i in range(np.max(self.G.nodes)+1)]
    #pos = [(self.nodes[i]["longitude"], self.nodes[i]["latitude"]) for i in self.G.nodes()]
    cols = [("blue" if i != self.init_id else "red") if self.nodes[i]["true_node"] else "green" for i in self.nodes()]
    
    
    # draw
    nx.draw(self.G, pos,
            node_color=cols, 
            node_shape='s', 
            node_size=15, 
            with_labels=False)  

def print_all_nodes(self):
    """
        Prints all node ids and their attributes - mainly for debugging purposes.
    """
    for i in self.nodes:
        print(i, ": ", self.G.nodes[i])