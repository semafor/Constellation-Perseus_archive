class PlanetarySystem():

    identifier = "genericsystem"
    criteria = []

    def __repr__(self):
        return "Planetary System"

    def __str__(self):
        if(self.active):
            status = "Active"
        else:
            status = "Inactive"

        return "%s %s %s" % (status, self.__repr__(), self._int_to_roman(self.get_level()))

    def __init__(self):

        self.active = False
        self.level = 1

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def set_level(self, level):
        assert not self._data_invariant()

        self.level = level

        assert not self._data_invariant()

    def get_level(self):
        return self.level

    def upgrade(self):
        self.set_level(self.level + 1)

    def downgrade(self):
        self.set_level(self.level - 1)

    def tick(self):
        pass

    def _data_invariant(self):
        if not __debug__:
            return None

        try:
            self.level + 1
        except:
            raise

        if(self.level < 1):
            raise AssertionError("Level lt 1: %s" % self.level)

    def _int_to_roman(self, integer):
        if type(integer) != type(1):
            raise TypeError("expected integer, got %s" % type(integer))
        if not 0 < integer < 4000:
            raise ValueError("Int %d not between 1 and 3999" % integer)
        ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
        nums = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
        result = ""
        for i in range(len(ints)):
            count = int(integer / ints[i])
            result += nums[i] * count
            integer -= ints[i] * count
        return result
