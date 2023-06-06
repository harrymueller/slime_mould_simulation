class Config():
    """
        Config class - basically just a dictionary but acccessing us conf.attr instead of conf["attr"]
    """
    def __init__(self, res: float, border_dist: list, func: object, t: float):
        self.res = res
        self.border_dist = border_dist
        self.func = func
        self.t = t