import fleet
import gameobject

from mission import DEFAULT_TRAVEL_TIME


class Player(gameobject.GameObject):
    def __init__(self, name=None,
            allotropes=0, ships=0, workforce=12,
            planetary=None, active=True):

        if not name:
            raise PlayerException("Needs name")

        self.name = name
        self.allotropes = allotropes
        self.ships = ships
        self.workforce = workforce
        self.planetary = planetary

        self.ships = []

        self.fleets = [
            fleet.Fleet(owner=self),
            fleet.Fleet(owner=self),
            fleet.Fleet(owner=self)
        ]

        self.fleets[0].assign_ships(self.ships)

        self.display_name = "%s, a stellar commander. Workforce: %d" \
            % (self.name, self.workforce)

    def get_fleet(self, index):
        return self.fleets[index]

    def get_fleets(self):
        return self.fleets

    def get_planetary(self):
        return self.planetary

    def set_planetary(self, planetary_id):
        self.data_invariant()

        self.planetary = planetary_id

        self.data_invariant()

    def get_ships(self):
        return self.ships

    def get_allotropes(self):
        return self.allotropes

    def get_workforce(self):
        return self.workforce

    def set_allotropes(self, allotropes):
        self.data_invariant()

        self.allotropes = allotropes

        self.data_invariant()

    def add_allotropes(self, amount):
        self.data_invariant()

        if(amount < 0):
            amount = 0

        self.set_allotropes(self.get_allotropes() + amount)

        self.data_invariant()

    def remove_allotropes(self, amount):
        self.data_invariant()

        current_amount = self.get_allotropes()
        diff = current_amount - amount

        if(amount < 0):
            amount = 0

        if(diff < 0):
            amount = current_amount

        self.set_allotropes(self.get_allotropes() - amount)

        self.data_invariant()

    def add_ships(self, ships, fleet_index):
        self.data_invariant()

        self.ships = self.ships + ships

        self.get_fleet(fleet_index).append_ships(ships)

        self.data_invariant()

    def remove_ship(self, ship):
        self.data_invariant()

        self.ships.remove(ship)

        self.data_invariant()

    def get_travel_time(self):
        return DEFAULT_TRAVEL_TIME

    def get_ship_total(self):
        total = 0
        for ship in self.ships:
            total = total + ship.get_points()

        return total

    def get_allotropes_per_tick(self):
        return len(self.get_ships()) + self.get_workforce() * 100

    def tick(self):
        self.data_invariant()

        #print "Tick on %s" % self.get_display_name()
        for fleet in self.get_fleets():
            mission = fleet.get_mission()
            if(mission):
                if(mission.get_stage() == "completed"):
                    fleet.set_mission(None)

            fleet.tick()
        self.add_allotropes(self.get_allotropes_per_tick())
        self.data_invariant()

    def data_invariant(self):

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

        if not type(self.ships) == type([]):
            raise ValueError("Player ships not a list: %s"\
                % str(self.ships))

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
