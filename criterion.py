class Criterion():
    """Represents a criterion"""
    def __str__(self):
        return "%s: %d" % (self.__repr__(), self.get_value())

    def __init__(self, value):

        self.value = value

    def get_value(self):
        return self.value

    def unmet(self):
        raise CriterionUnmetError("Unmet %s" % self.__repr__())


class StellarClassCriterion(Criterion):
    def __repr__(self):
        return "Stellar Class Criterion"


class CriterionUnmetError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
