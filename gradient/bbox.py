import numpy as np
import math

def _set_bbox(self):
    """
        Finds the bounding box of the nodes
        Same code as slime/methods/bbox
    """
    # initialise search arrays
    lat = self._find_min_max_attr("latitude")
    lon = self._find_min_max_attr("longitude")

    for i in [0, 1]:
        lat[i] += self.conf.border_dist[0] * (1 if i == 1 else -1)
        lon[i] += self.conf.border_dist[1] * (1 if i == 1 else -1)

    self.bbox = {"latitude": lat, "longitude": lon}
    
    # round
    for i in ["latitude", "longitude"]:
        for (j, func) in enumerate([math.floor, math.ceil]):
            self.bbox[i][j] = func(self.bbox[i][j]/self.conf.res)*self.conf.res

def _find_min_max_attr(self, attr: str):
    """
        Finds the smallest and largest values of a given node attribute
        Same code as slime/methods/bbox
    """
    vals = [self.nodes[list(self.nodes)[0]][attr], self.nodes[list(self.nodes)[0]][attr]]

    for u in list(self.nodes)[1:]:
        if self.nodes[u][attr] < vals[0]: vals[0] = self.nodes[u][attr]
        elif self.nodes[u][attr] > vals[1]: vals[1] = self.nodes[u][attr]

    return np.array(vals, dtype = np.float64)