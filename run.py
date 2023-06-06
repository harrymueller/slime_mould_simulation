# Libraries
from time import time
import numpy as np
import pandas as pd
import math
import networkx as nx

# Classes and functions
from london_tube import LondonTubeData
from gradient import Gradient
from slime import SlimeNetwork
from mst import MST
from performance import Performance
from sigmoid import make_sigmoid_functions

# constants
DIR = "data"
FILES = {"stations": "london.stations.csv", 
         "connections": "london.connections.csv",
         "lines": "london.lines.csv"}
OUT = "results.csv"

# Hyperparameters
R = 6371 # earth radius in km
ZONES = [1, 1.5, 2] # testing three different zones
ID = 259 # initial station id
N_RUNS = 10

# set random seed
np.random.seed(3141)

# get london tube data and sigmoid function
ltdat = LondonTubeData(DIR, FILES)
inv_sigmoid, sigmoid = make_sigmoid_functions(-3,1)

df = None

# for each zone
for z in ZONES:
    print("Zone %d" % (z))
    # subset london tubes
    ltdat.subset(zones = z)
    ltdat.set_init(id = ID)

    # establish gradient
    print("Establishing gradient")
    grad = Gradient(ltdat.G, res = 0.0001, border_dist = [1e-3, 2e-3], func = sigmoid, t = sigmoid(2))

    # London Tubes performance
    p = Performance(ltdat.G, name = "London Tubes", zones = z).to_df()
    if df is None: df = p
    else: df = pd.concat([df, p])

    for use_g in [False, True]:
        print("%sUsing Gradient" % ("" if use_g else "Not "))
        # Slime Mould performance
        for i in range(N_RUNS):
            print("Run %d" % (i))
            t1 = time()

            slime = SlimeNetwork(ltdat.G, ltdat.init["id"])
            if use_g: slime.set_gradient(grad)
            slime.set_config(seed = None, growth_dist = 0.2, seeing_dist = 0.2, 
                            border_dist = [1e-3, 2e-3], R = R, accuracy = 5, dist_measure = "Haversine")
            slime.grow(n_branches = 10, n_attempts = 20, until_connected = True, verbose = False)
            slime.trim()
           
            if nx.is_connected(slime.G): 
                p = Performance(slime.G, name = "Slime Mould", run = i, time = time() - t1, 
                                        zones = z, other = "gradient" if use_g else "").to_df()
                df = pd.concat([df, p])

    # MST performance
    t1 = time()
    mst = MST(ltdat.G, ltdat.init["id"])
    mst.add_all_edges()
    mst.apply_mst()
        
    p = Performance(mst.G, name = "MST", run = i, time = time() - t1, zones = z).to_df()
    df = pd.concat([df, p])

    df.to_csv(OUT, index = False)

print("Saving to CSV (%s)" % (OUT))
df.to_csv(OUT, index = False)
