import os
import pandas as pd
import numpy as np
from collections import deque

from haversine import calculate_distance
from .data import Data

class LondonTubeData():
    # imports
    from .graph import _construct_graph, plot, get_graph

    def __init__(self, path: str, files: dict, R = 6371):
        self._load_data(path, files, R)
        self.init = None
    
    def _load_data(self, path: str, files: dict, R: float):
        """
            Loads the raw data
        """
        # load three files using pandas
        data = {name: pd.read_csv(os.path.join(path, files[name])) for name in ["stations", "connections", "lines"]}

        # set index
        data["stations"].index = data["stations"]["id"]

        # get positions as dict
        data["positions"] = data["stations"][["longitude", "latitude"]].apply(tuple, axis = 1).to_dict()

        self.raw_data = Data(**data)
        self._connection_weights(R)
    
    def _connection_weights(self, R: float):
        """
            Add connection weights to connections
        """
        stations = self.raw_data.stations
        
        def dist(r):
            ll1 = {"latitude": np.double(stations["latitude"][stations["id"] == r["station1"]]),
                   "longitude": np.double(stations["longitude"][stations["id"] == r["station1"]])}

            ll2 = {"latitude": np.double(stations["latitude"][stations["id"] == r["station2"]]),
                   "longitude": np.double(stations["longitude"][stations["id"] == r["station2"]])}

            return calculate_distance(ll1, ll2, R, False)

        self.raw_data.connections["weight"] = self.raw_data.connections.apply(dist, axis  = 1)
    
    def subset(self, zones = None, ids = [], n_stations = None):
        """
            Creates a subset of the data based on zones (int) or a list of station IDs or n_stations
        """
        data = Data()
        
        # subset stations based on zones or ids
        if zones: mask = self.raw_data.stations["zone"] <= zones
        elif ids: mask = self.raw_data.stations["id"].isin(ids)
        elif n_stations: mask = self.raw_data.stations["id"].isin(self._get_n_stations(n_stations))
        else: raise Exception("Requires either zones or IDs.") # if neither params passed, raise exception
        
        data.stations = self.raw_data.stations[mask]
        
        # get valid ids
        self.ids = data.stations["id"]

        # subset connections
        data.connections = self.raw_data.connections[self.raw_data.connections["station1"].isin(self.ids)]
        data.connections = data.connections[data.connections["station2"].isin(self.ids)]

        # subset lines
        data.lines = self.raw_data.lines[self.raw_data.lines["line"].isin(data.connections["line"].unique())]
        
        # positions
        data.positions = {i: self.raw_data.positions[i] for i in self.raw_data.positions if i in self.ids}
        
        self.data = data
        self._construct_graph()
        
    def _get_n_stations(self, n_stations: int):
        """
            Returns the ids of connected stations from the init station
        """
        if self.init is None: raise Exception("Initialisation must be set prior to subsetting with n stations.")

        ids = []
        to_visit = deque([self.init["id"]])
        
        # small func to return list of all connected stations
        def get_connected_stations(connections: pd.DataFrame, id: int):
            return (list(connections["station2"][connections["station1"] == id]) + 
                    list(connections["station1"][connections["station2"] == id]))
        
        # until list of ids is full
        while len(ids) < n_stations:
            id = to_visit.pop()
            for new_id in get_connected_stations(self.raw_data.connections, id):
                if len(ids) == n_stations: break
                if new_id not in ids: # check new is not already added, then add to ids and queue
                    ids.append(new_id)
                    to_visit.append(new_id)
        
        return ids

    def get(self):
        """
            Returns the four variables separately (stations, connections, lines, positions)
        """
        return self.data.get()
    
    def set_init(self, max_col = False, id = False, prior_subsetting = False):
        """
            Returns the station name and id for the initial station.
            
            @param use_max: String - the station with the maximum of this column is chosen
            @param use_id: int - station id
            @param prior_subsetting: bool - if set before subsetting data
        """
        dat = self.raw_data if prior_subsetting else self.data
        if max_col: 
            max_val = np.max(dat.stations[max_col])
            self.init = dat.stations[dat.stations[max_col] == max_val].iloc[0]
        elif id: 
            self.init = dat.stations[dat.stations["id"] == id].iloc[0]
        else:
            raise Exception("Either max_col or id is required.")