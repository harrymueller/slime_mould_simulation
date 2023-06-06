from ..libs import *
from collections import deque
from math import sin, cos, asin, atan2, pi, radians, degrees
from .haversine import calculate_position

# graph growing
def reset_graph(self):
    """
        Removes all grown nodes - keeps true nodes
    """
    self.G.remove_nodes_from([u for u in self.nodes if not self.nodes[u]["true_node"]])
    self.connect_all()
    

def grow(self, n_branches = 3, n_attempts = 5, n_growths = 10, until_connected = False, verbose = False):
    """
        Grow network

        @param n_branches: max number of branches per growth node
            Can be None -> will keep growing nodes till n_attemts
        @param n_attempts: max number of attempts at growing per growth node
        @param n_growths:  number of growth nodes to grow from, inc initial node
        @param until_connected: ignores n_growths and grows until all true nodes are found
    """
    # set seed - for repeatability
    np.random.seed(self.conf.seed)
    
    # init parent queue - FIFO
    try: self.parents
    except:
        parents = deque() 
        parents.append(self.init_id)
        self.found_nodes = set([-1, self.init_id]) # -1 inc. for no gradient
    else:
        parents = self.parents

    # init new id
    new_id = 0
    
    if not n_branches: n_branches = np.inf
    
    # repeat until connected if until_connected is True,
    # else repeat for number of growth cycles
    n = 0
    while until_connected and not nx.is_connected(self.G) or (n < n_growths and not until_connected):
        # find next empty node
        while new_id in self.nodes: new_id += 1

        new_id, parents = self._growth_cycle(new_id, parents, n_branches, n_attempts)

        # increase num growths
        n +=1

        # no more parent nodes to grow from
        if not parents: break 
        if verbose and n % 100 == 0: print(n)

    self.parents = parents
    self.growth_cycles += n
    return {"num_growth_cycles": n}



def _growth_cycle(self, new_id: int, parents: deque, n_branches: int, n_attempts: int):
    """
        Executes one full growth cycle
    """
    # iterators
    i_branches = 0
    i_attempts = 0
    
    parent = parents.popleft()
    
    # invalid parent - outside of bbox
    if not self.check_node_in_bbox(parent): return (new_id, parents)
        
    # while less than max branches and max attempts
    while i_branches < n_branches and i_attempts < n_attempts:
        ll = self._grow_node(new_id, parent)
        if ll is not None:
            # add node
            self.G.add_node(new_id, 
                            latitude = ll["latitude"], 
                            longitude = ll["longitude"],
                            true_node = False)
            
            # add edge from parent
            self._add_edge(parent, new_id)

            # add this node to parent queue
            parents.append(new_id)
            
            # increase counters
            i_branches+=1
            #new_id +=1
                                
        i_attempts+=1

    return (new_id, parents)


def _grow_node(self, new_id: int, parent: int):
        """
            Grows a new node from the parent node
            Returns None if the new node is invalid, or (lat, lon) if it is
        """
        # proportion of growth distance that is random
        prop = 1 
        ll = self.nodes[parent]

        if self.use_gradient:
            grad = self.gradient.access(ll["latitude"], ll["longitude"])
            # if valid node and the node creating the gradient has not been found, apply force
            if grad[2] not in self.found_nodes:
                ll = calculate_position(ll, self.conf.growth_dist*grad[0], grad[1], 
                                        self.conf.accuracy, self.conf.R, self.conf.use_eucl)
                prop -= grad[0]
                #print(grad)
        #print(prop)
        ll = calculate_position(ll, self.conf.growth_dist*prop, np.random.random() * 2 * pi, 
                                self.conf.accuracy, self.conf.R, self.conf.use_eucl)

        if not ((self.bbox["latitude"][0] <= ll["latitude"] <= self.bbox["latitude"][1] and
            self.bbox["longitude"][0] <= ll["longitude"] <= self.bbox["longitude"][1])): return None

        found = []

        # loop through all nodes currently in network
        for j in self.nodes:
            # check if any nodes within seeing dist
            if j != parent and self._calc_dist_nodes(ll, self.nodes()[j]) < self.conf.seeing_dist:
                # if a true node is, add true node id to found
                if self.nodes[j]["true_node"] and j != self.init_id:
                    found.append(j)
                # but if its a grown node, dont add this node and try again
                else:
                    return None

        # add edge from found nodes
        for f in found: self._add_edge(new_id, f, ll)
        # add all found nodes
        self.found_nodes = self.found_nodes.union(found)
        
        return ll