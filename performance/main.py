import networkx as nx
import numpy as np
import pandas as pd

class Performance():
    """
        Class wrapper for performance measures
    """
    def __init__(self, G, name, run = -1, time = np.nan, zones = np.nan, other = ""):
        self.G = G
        self.name = name
        self.run = run
        self.time = time
        self.zones = zones
        self.other = other

        self.analyse()
        
    def get_cost(self):
        return self.G.size(weight="weight")
    
    def get_travel_time(self):
        return nx.average_shortest_path_length(self.G, weight = "weight")
    
    def get_vulnerability(self):
        """
            Gets number of vulnerable connections (edges that disconnect the graph), 
            and the average travel time if it doesn't disconnect the graph.
            
            Returns ([num vulnerable, num redundant],
                     [list of travel times (len = num redundant)])
        """
        # record number of vulnerable edges -> disconnect graph
        n = 0

        # for redundant edges -> record travel time
        times = []

        # for each edge
        for (u,v) in self.G.edges:
            w = self.G[u][v]["weight"] # save weight for readding
            self.G.remove_edge(u,v) 

            # if graph remains connected - calc travel time
            if nx.is_connected(self.G): times.append(self.get_travel_time())
            else: n += 1

            self.G.add_edge(u,v,weight = w)

        return([n, len(self.G.edges)-n],times)
    
    def analyse(self):
        self.cost = self.get_cost()
        self.ttime = self.get_travel_time()
        self.vuln = self.get_vulnerability()
    
    def print(self):
        print("Cost = %f" % (self.cost))
        print("Travel Time = %f" % (self.ttime))
        print("Vulnerable Edges = %d" % (self.vuln[0][0]))
        print("Redundant Edges = %d (+%f)" % (self.vuln[0][1], np.nan if self.vuln[0][1] == 0 else np.nanmean(self.vuln[1])-self.ttime))
        print("Prop of Vulnerable Edges = %f" % (self.vuln[0][0]/(self.vuln[0][0] + self.vuln[0][1])))
            
    def to_csv(self, filename):
        with open(filename, "w") as f:
            f.write("cost,%f\n" % (self.cost))
            f.write("time,%f\n" % (self.time))
            f.write("v_edges,%d\n" % (self.vuln[0][0]))
            f.write("r_edges,%d\n" % (self.vuln[0][1]))
            
            for (i, x) in enumerate(self.vuln[1]):
                f.write("v_time_%d,%f\n" % (i,x))

    def to_df(self):
        df = pd.DataFrame([{
            "name": self.name,
            "run" : self.run,
            "time": self.time,
            "zones": self.zones,
            "other": self.other,
            "cost": self.cost,
            "ttime": self.ttime,
            "v_edges": self.vuln[0][0],
            "r_edges": self.vuln[0][1],
            "mean_increase": np.nan if self.vuln[0][1] == 0 else np.nanmean(self.vuln[1])-self.ttime
        }])
        return df.astype(dtype = {
            "name": str,
            "run" : int,
            "time": np.double,
            "zones": np.double,
            "other": str,
            "cost": np.double,
            "ttime": np.double,
            "v_edges": int,
            "r_edges": int,
            "mean_increase": np.double
        })