# Slime Mould Simulation

Harrison Mueller - 22732927

## Description
My implementation of a Slime Mould simulation uses several classes:
 - `LondonTubeData`; Loads, subsets, and plots the LondonTubeData
 - `Gradients`: Creating and accessing a 3D array filled with the gradient magnitude and direction, as well as the node the gradient points to
 - `Slime`: Slime mould simulation - configuration, growing and trimming the network
 - `MST`: Apply the minimum-spanning tree algorithm to the fully-connected version of the graph
 - `Performance`: Calculates three metrics given a graph, and returns in the form of a pandas DF

And a few stand-alone python scripts:
 - `haversine.py`: Functions for calculating distance, bearing and new position of points using latitude and longitude
 - `sigmoid.py`: Stores a function for creating sigmoid functions (and their inverse)
 - `run.py`: Runs through different zones and simulates the network several times whilst recording performance

### Results
Saved under `results`.

### Data
Available under `data`, or from https://github.com/nicola/tubemaps.

## Use
### Pip Environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running all simulations
```
python3 run.py
```

### Running the Jupyter Notebook
```
jupyter notebook slime_mould_simulation.ipynb
```