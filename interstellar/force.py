class Force():
    """Represents a list of fleets
    """
    def __init__(self, fleets):

        # convert single fleet to list
        try:
            if(fleets.get_ships()):
                fleets = [fleets]
        except:
            pass

        self.fleets = fleets

        # remove fleets without ships
        self.remove_empty_fleets()

        assert not self._data_invariant()

    def get_fleets(self):
        return self.fleets

    def get_all_ships(self):
        ships = []
        for fleet in self.get_fleets():
            for ship in fleet.get_ships():
                ships.append(ship)

        return ships

    def get_all_ships_ordered(self, criterion, reverse=False):
        ships = []
        for fleet in self.get_fleets():
            ships = ships + fleet.get_ships_ordered_by(criterion, reverse)

        return ships

    def get_warm_guns(self):
        guns = 0
        for ship in self.get_all_ships():

            # TODO: count on fleet to sort this out
            if not ship.is_hull_intact():
                raise Exception("Broken ship was included in force")

            guns = guns + len(ship.get_wam_guns())

        return guns

    def remove_fleet(self, fleet):
        assert not self._data_invariant()

        self.fleets.remove(fleet)

        assert not self._data_invariant()

    def remove_empty_fleets(self):
        assert not self._data_invariant()

        for index, fleet in enumerate(self.get_fleets()[:]):
            if(len(fleet.get_ships()) == 0):
                self.remove_fleet(fleet)

        assert not self._data_invariant()

    def _data_invariant(self):
        if not __debug__:
            return None

        try:
            for fleet in self.fleets:
                fleet.get_ships()
        except:
            raise

        for fleet in self.fleets:
            if(self.fleets.count(fleet) > 1):
                raise AssertionError("fleet %s not unique (appeas %d times)"\
                    % (str(fleet), self.fleets.count(fleet)))
