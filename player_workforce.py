class PlayerWorkforce():
    """Represents the players workforce.
        The workforce mans the various systems
    """
    def __str__(self):
        return "Workforce, %d strong, belonging to %s"\
            % (self.size, self.owner.get_name())

    def __repr__(self):
        return "Workforce"

    def __init__(self, owner, size):

        self.owner = owner

        self.size = size

        self.statuses = {
            "free": size,
            "occupied": 0,
            "disabled": 0
        }

        assert not self._data_invariant()

    def add_workforce(self, n):
        assert not self._data_invariant()

        self.size = self.size + n
        self.statuses["free"] = self.statuses["free"] + 1

        assert not self._data_invariant()

    def use_workforce(self, amount):
        """Return True if workforce is now in use, False if not enough free"""
        assert not self._data_invariant()

        if(amount > self.get_free()):
            return False

        self.statuses["free"] = self.statuses["free"] - amount
        self.statuses["occupied"] = self.statuses["occupied"] + amount

        assert not self._data_invariant()

        return True

    def free_workforce(self, amount):
        assert not self._data_invariant()

        self.statuses["free"] = self.statuses["free"] + amount
        self.statuses["occupied"] = self.statuses["occupied"] - amount

        assert not self._data_invariant()

    def disable_workforce(self, amount):
        """Disables free, then occupied workforce"""
        assert not self._data_invariant()

        self.statuses["free"] = self.get_free() - amount

        if(self.get_free() < 0):
            # free occupied workforce
            self.statuses["occupied"]\
                = self.statuses["occupied"] - self.get_free()

            # free now 0
            self.statuses["free"] = 0

        assert not self._data_invariant()

    def get_free(self):
        return self.statuses["free"]

    def get_occupied(self):
        return self.statuses["occupied"]

    def get_disabled(self):
        return self.statuses["disabled"]

    def get_size(self):
        return self.size

    def _data_invariant(self):
        if not __debug__:
            return None

        if(self.size < 0):
            raise AssertionError("Size lt 0")

        # make sure statuses match size
        statuscount = 0
        for k, v in self.statuses.iteritems():
            statuscount = statuscount + v

        if(statuscount != self.size):
            raise AssertionError("Size and statuscount differ")
