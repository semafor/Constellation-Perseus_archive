import fleet
import gameobject

from mission import DEFAULT_TRAVEL_TIME


class Player(gameobject.GameObject):
    def __str__(self):
        """Return string representation of player object."""
        return "Player:\t" + self.name + \
            "\n\tAllotropes:\t" + str(self.allotropes) + \
            "\n\tShips:\t\t" + str(len(self.get_ships())) + \
            "\n\tWorkforce:\t" + str(self.workforce) + \
            "\n\tPlanetary:\t" + str(self.planetary)

    def __init__(self, name=None,
            allotropes=0, workforce=12,
            planetary=None, active=True):

        if not name:
            raise PlayerException("Needs name")

        self.name = name
        self.allotropes = allotropes
        self.workforce = workforce
        self.planetary = planetary

        self.fleets = [
            fleet.Fleet(owner=self),
            fleet.Fleet(owner=self),
            fleet.Fleet(owner=self)
        ]

        self.display_name = "%s, a stellar commander. Workforce: %d" \
            % (self.name, self.workforce)

    def get_fleet(self, index):
        return self.fleets[index]

    def get_fleets(self):
        return self.fleets

    def get_planetary(self):
        return self.planetary

    def set_planetary(self, planetary_id):
        if __debug__:
            self.data_invariant()

        self.planetary = planetary_id

        if __debug__:
            self.data_invariant()

    def get_ships(self):
        ships = []

        for fleet in self.get_fleets():
            ships = ships + fleet.get_ships()

        return ships

    def get_allotropes(self):
        return self.allotropes

    def get_workforce(self):
        return self.workforce

    def set_allotropes(self, allotropes):
        if __debug__:
            self.data_invariant()

        self.allotropes = allotropes

        if __debug__:
            self.data_invariant()

    def add_allotropes(self, amount):
        if __debug__:
            self.data_invariant()

        if(amount < 0):
            amount = 0

        self.set_allotropes(self.get_allotropes() + amount)

        if __debug__:
            self.data_invariant()

    def remove_allotropes(self, amount):
        if __debug__:
            self.data_invariant()

        current_amount = self.get_allotropes()
        diff = current_amount - amount

        if(amount < 0):
            amount = 0

        if(diff < 0):
            amount = current_amount

        self.set_allotropes(self.get_allotropes() - amount)

        if __debug__:
            self.data_invariant()

    def add_ships(self, ships, fleet_index):
        if __debug__:
            self.data_invariant()

        self.get_fleet(fleet_index).append_ships(ships)

        if __debug__:
            self.data_invariant()

    def get_travel_time(self):
        return DEFAULT_TRAVEL_TIME

    def get_ship_total(self):
        total = 0
        for ship in self.get_ships():
            total = total + ship.get_points()

        return total

    def get_allotropes_per_tick(self):
        return len(self.get_ships()) + self.get_workforce() * 100

    def tick(self):
        if __debug__:
            self.data_invariant()

        #print "Tick on %s" % self.get_display_name()
        for fleet in self.get_fleets():
            mission = fleet.get_mission()
            if(mission):
                if(mission.get_stage() == "completed"):
                    fleet.set_mission(None)

            fleet.tick()

        self.add_allotropes(self.get_allotropes_per_tick())

        if __debug__:
            self.data_invariant()

    def data_invariant(self):
        if not __debug__:
            return None

        # name
        if not type(self.name) == type(""):
            raise ValueError("Player name must be a str " % str(self.name))
        elif(self.name == ""):
            raise ValueError("Player name must be more than 0 characters: %s"\
                % str(self.name))

        # allotropes
        if not type(self.allotropes) == type(1):
            raise ValueError("Allotropes not an int  %s"\
                % str(self.allotropes))
        elif(self.allotropes < 0):
            raise ValueError("Allotropes is a negative int %s"\
                % str(self.allotropes))

        # workforce
        if not type(self.workforce) == type(1):
            raise ValueError("Player workforce not int: %s"\
                % str(self.workforce))
        elif(self.workforce < 0):
            raise ValueError("Player workforce less than 0: %s"\
                % str(self.workforce))

        # planetary
        try:
            self.planetary.get_owner()
        except:
            raise ValueError("Player planetary not a planetary: %s"\
                % str(self.planetary))

        # fleets
        try:
            self.fleets[0].get_mission()
        except:
            raise ValueError("Player has no first fleet: %s"\
                % str(self.fleets[0]))


class PlayerException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
