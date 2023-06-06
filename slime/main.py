from .libs import *
from .config import Config

class SlimeNetwork:
    """
        Slime Network class that simulates a slime growing a network over geographical locations.
    """
    # import methods
    from .methods.helpers import _all_pairs, _calc_dist_nodes, _connect_all, _add_edge
    from .methods.displaying import plot, print_all_nodes
    from .methods.growing import reset_graph, grow, _growth_cycle, _grow_node
    from .methods.trim import trim, _remove_unneeded_nodes, _remove_unneeded_edges, _trim_redundant, _add_false_edges, _true_shortest_paths
    from .methods.bbox import set_bbox, find_min_max_attr, check_node_in_bbox
    from .config import set_config, print_config

    # INIT
    def __init__(self, init_graph, init_id):
        """
            Initialise the network based on the graph given. 
        """
        self.G = nx.Graph() # init graph
        self.nodes = self.G.nodes # shortcut for getting nodes
        self.init_id = init_id

        # add real nodes
        for (i, g_id) in enumerate(init_graph.nodes()):
            self.G.add_node(g_id, #i+1 if g_id != init_id else 0, 
                            latitude = init_graph.nodes[g_id]["latitude"], 
                            longitude = init_graph.nodes[g_id]["longitude"],
                            true_node = True)
        
        # set up config
        self.conf = Config()
        self.set_config()
        
        # set bounding box and growth cycle counter
        self.set_bbox()
        self.growth_cycles = 0

        self.use_gradient = False

    def set_gradient(self, gradient: object):
        """
            Set the model to use the gradient obj provided
        """
        self.use_gradient = True
        self.gradient = gradient

    
        
        
    
    
           
        
        
    