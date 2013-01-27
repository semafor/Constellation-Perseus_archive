class Cost():
    """Represents a cost"""
    def __str__(self):
        return "%s: %d" % (self.__repr__(), self.get_value())

    def __init__(self, value, refundable=False):

        self.refundable = refundable
        self.value = value

        self._deducted = False

    def set_deducted(self, deducted):

        if(deducted):
            self._deducted = True
        else:
            self._deducted = False

    def is_deducted(self):
        return self._deducted

    def is_refundable(self):
        return self.refundable

    def get_value(self):
        return self.value

    def set_value(self, val):
        if not type(val) == type(1):
            raise ValueError("%s not int" % str(val))

        if val < 0:
            val = 0

        self.value = val

    def unsuccessful(self):
        raise CostUnmetError("Unmet %s" % self.__repr__())

    def get_multiplied_value(self, coefficient):
        return self.get_value() * coefficient


class WorkforceCost(Cost):
    def __repr__(self):
        return "Workforce Cost"


class AllotropeCost(Cost):
    def __repr__(self):
        return "Allotrope Cost"


class CostUnmetError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
