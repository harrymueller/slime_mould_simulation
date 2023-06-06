class Data():
    """
        Object that stores the four variables required
    """
    stations = None
    connections = None
    lines = None
    positions = None
    
    def __init__(self, stations = None, connections = None, lines = None, positions = None):
        self.stations = stations
        self.connections = connections
        self.lines = lines
        self.positions = positions
        
    def get(self):
        return (self.stations, self.connections, self.lines, self.positions)
