import matplotlib.pyplot as plt

def _get_ll(self, i: int, j: int):
    """
        Returns lat and lon of a cell in the array
    """
    return {"longitude": self.bbox["longitude"][0] + self.conf.res*j,
            "latitude": self.bbox["latitude"][0] + self.conf.res*i}

def _get_coords(self, lat: float, lon: float):
    """
        Returns the coords of the cell that represents the given lat lon
    """
    return (round((lat-self.bbox["latitude"][0])/self.conf.res),
            round((lon-self.bbox["longitude"][0])/self.conf.res))

def plot(self):
        """
            Plot the arrays
        """
        fig, ax = plt.subplots(3, figsize=(6, 8))
        names = ["Magnitude", "Direction", "Node"]
        for i in range(3):
            ax[i].imshow(self.arr[:,:,i])
            ax[i].set(xticks = [], yticks = [], title = names[i])

def access(self, lat: float, lon: float):
    """
        Get the magnitude, bearing, and node for a given lat and lon
    """
    if (self.bbox["latitude"][0] <= lat <= self.bbox["latitude"][1] and
        self.bbox["longitude"][0] <= lon <= self.bbox["longitude"][1]):
        return self.arr[self._get_coords(lat,lon)]
    else: return [0,0,-1]
