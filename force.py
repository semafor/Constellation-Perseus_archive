from random import shuffle


class Force():
    def __init__(self, fleets):

        try:
            if(fleets.get_ships()):
                fleets = [fleets]
        except:
            pass

        try:
            for fleet in fleets:
                fleet.get_ships()
        except:
            raise TypeError("fleets is not a list of fleets: %s"\
                % str(fleets))

        for fleet in fleets:
            if(fleets.count(fleet) > 1):
                raise DuplicateFleetError("fleet %s appears %d times"\
                    % (str(fleet), fleets.count(fleet)))

        self.fleets = fleets

        # remove fleets without ships
        self.remove_empty_fleets()

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

            if not ship.is_hull_intact():
                raise Exception("Broken ship was included in force")

            guns = guns + len(ship.get_wam_guns())

        return guns

    def remove_fleet(self, fleet):
        self.fleets.remove(fleet)

    def remove_empty_fleets(self):
        for index, fleet in enumerate(self.get_fleets()[:]):
            if(len(fleet.get_ships()) == 0):
                self.remove_fleet(fleet)


class DuplicateFleetError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
