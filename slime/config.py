from .libs import *

class Config:
    """
        Config class - basically just a dictionary but acccessing us conf.attr instead of conf["attr"]
    """
    def update(self, seed, seeing_dist, growth_dist, border_dist, dist_measure, accuracy, R):
        self.seed = seed
        self.seeing_dist = seeing_dist
        self.growth_dist = growth_dist
        self.border_dist = border_dist
        self.dist_measure = dist_measure
        self.use_eucl = self.dist_measure == "Euclidean"
        self.accuracy = accuracy
        self.R = R


 # CONFIG
def set_config(self, seed = None, seeing_dist = 0.4, growth_dist = 0.3, border_dist = [0.05, 0.10],
                     dist_measure = "Euclidean", accuracy = 5, R = 6371):
    """
        Update the config (wrapper for Config.update)

        @param seed: random seed used when growing (None = random)
        @param seeing_dist: distance at which a node can "see" others
        @param growth_dist: distance at which new nodes are added
        @param dist_measure: Whether to use euclidean or haversine distance calculations
            Options = ["Euclidean", "Haversine"]
        @param accuracy: Number of DP when calculate new positions 
    """
    if not seed: seed = np.uint32(np.random.random() * 2**32)
    np.random.seed(seed)
    if seeing_dist < growth_dist: print("WARNING: growth_dist should be less than seeing_dist for optimal results.")
    self.conf.update(seed, seeing_dist, growth_dist, border_dist, dist_measure, accuracy, R)

def print_config(self):
    """
        Prints the configuration variables
    """
    print("#"*30 + "\n# CONFIG #\n" + "#" * 30)
    print("Seed: %i" % self.conf.seed)
    print("Seeing Distance: %.3f" % self.conf.seeing_dist)
    print("Growth Distance: %.3f" % self.conf.growth_dist)
    print("Border Distance: %.3f" % self.conf.border_dist)
    print("Distance Measure: %s" % self.conf.dist_measure)
    print("R: %f" % self.conf.R)

