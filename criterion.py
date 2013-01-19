class Criterion():
    """Represents a criterion"""
    def __init__(self, value, refundable=False):

        self.refundable = refundable
        self.value = value

        self._deducted = False

    def get_value(self):
        val = self.value

        return val

    def is_refundable(self):
        return self.refundable and self._deducted

    def unmet(self):
        raise CriterionUnmetError("Unmet %s" % self.__repr__())


class WorkforceCriterion(Criterion):
    def __repr__(self):
        return "Workforce Criterion"

    def met(self, player):
        if not self.get_value() <= player.get_workforce().get_free():
            self.unmet()

    def deduct(self, player):
        self.met(player)

        if not self._deducted:
            player.get_workforce().use_workforce(self.get_value())
            self._deducted = True

    def refund(self, player):
        if self.is_refundable():
            player.get_workforce().free_workforce(self.get_value())
            self._deducted = False


class AllotropeCriterion(Criterion):
    def __repr__(self):
        return "Allotrope Criterion"

    def met(self, player):
        if not self.get_value() <= player.get_allotropes():
            self.unmet()

    def deduct(self, player):
        self.met(player)

        if not self._deducted:
            player.set_allotropes(player.get_allotropes() - self.get_value())
            self._deducted = True

    def refund(self, player):
        if self.is_refundable():
            player.set_allotropes(player.get_allotropes() + self.get_value())
            self._deducted = False


class StellarClassCriterion(Criterion):
    def __repr__(self):
        return "Stellar Class Criterion"

    def met(self, player):
        if not player.get_planetary().stellar_class >= self.get_value():
            self.unmet()


class CriterionUnmetError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
