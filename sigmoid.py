import math

def make_sigmoid_functions(c1: float, c2: float):
    """
        Creates the inverse sigmoid and sigmoid function given c1 and c2
    """
    def inv_sig(y):
        return math.log(1/y-1)/(-c1)+c2
    def sigmoid(x):
        return 1 / (1 + math.exp(-c1 * (x - c2)))
    return (inv_sig, sigmoid)