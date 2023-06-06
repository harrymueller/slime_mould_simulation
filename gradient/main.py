import networkx as nx
import numpy as np

from .config import Config
from haversine import calculate_distance, calculate_bearing

class Gradient():
    """
        Creates and allows access to a 3D array containing magnitude and direction to the nearest node
    """

    from .bbox import _set_bbox, _find_min_max_attr
    from .accessors import _get_ll, _get_coords, plot, access

    def __init__(self, G, res = 0.1, border_dist = [0.1,0.2], func = None, t = 0.1):
        #graph
        self.G = G
        self.nodes = self.G.nodes
        
        # config
        if func is None: raise Exception("Requires function to convert distance to magnitude.")
        self.conf = Config(res, border_dist, func, t)
        
        self._set_bbox()
        self._init_arr()
        self._calc_gradients()
    
    def _init_arr(self):
        """
            Constucts the array
        """
        shape = np.array([self.bbox["latitude"][1] - self.bbox["latitude"][0],
                          self.bbox["longitude"][1] - self.bbox["longitude"][0]])
        shape /= self.conf.res
        shape = np.ceil(shape+1).astype(int)
        self.shape = shape # save shape
        self.arr = np.zeros((*shape, 3), dtype = np.double) # create array
        self.arr[:,:,2] = -1

    def _calc_gradients(self):
        """
            Calculates gradients
        """
        # for each cell and each node
        # NOT optimal - checks the distance from every cell to every node
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                # get lat and lon of this cell
                ll = self._get_ll(i,j)
                
                # for each node
                for n in self.nodes:
                    # calculate distance (magnitude), and bearing
                    d = calculate_distance(ll, self.nodes[n], use_eucl = False)
                    b = calculate_bearing(ll, self.nodes[n], use_eucl = False)
                    m = self.conf.func(d)
                    
                    # if magnitude above threshold and greater than current magnitude
                    if m > self.conf.t and m > self.arr[i,j,0]:
                        self.arr[i,j] = [m, b, n]
    
    
    
    