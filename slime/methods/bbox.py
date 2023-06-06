import numpy as np

def set_bbox(self):
    """
        Finds the bounding box of the nodes
    """
    # initialise search arrays
    lat = self.find_min_max_attr("latitude")
    lon = self.find_min_max_attr("longitude")
    
    for i in [0, 1]:
        lat[i] += self.conf.border_dist[0] * (1 if i == 1 else -1)
        lon[i] += self.conf.border_dist[1] * (1 if i == 1 else -1)
    
    self.bbox = {"latitude": lat, "longitude": lon}
    
def find_min_max_attr(self, attr: str):
    """
        Finds the smallest and largest values of a given node attribute
        Same code as gradient/bbox
    """
    vals = [self.nodes[list(self.nodes)[0]][attr], self.nodes[list(self.nodes)[0]][attr]]

    for u in list(self.nodes)[1:]:
        if self.nodes[u][attr] < vals[0]: vals[0] = self.nodes[u][attr]
        elif self.nodes[u][attr] > vals[1]: vals[1] = self.nodes[u][attr]

    return vals

def check_node_in_bbox(self, i: int):
    """
        Checks if the given node is in the bounding box of the graph
    """
    for m in ["latitude", "longitude"]:
        if self.nodes[i][m] < self.bbox[m][0] or self.nodes[i][m] > self.bbox[m][1]:
            return False
        
    return True