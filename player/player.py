from interstellar import fleet, mission
import gameobject

from workforce import Workforce


class Player(gameobject.GameObject):
    """Represents players

    Exceptions:
        PlayerNeedsNameError
            Raised when player name is invalid
    """
    def __str__(self):
        """Return string representation of player object."""

        return "\n=========================\nPlayer:\t %s\n=========================\n\
            \n\tAllotropes:\t%d\
            \n\tShips:\t\t%d\
            \n\tWorkforce:\t%d (Free: %d, Occupied: %d, Disabled: %d)\
            \n\tPlanetary:\t%s\
            \n\n\tFleets:\
            \n\t#1:\
            \t\t%s\
            \n\t#2:\
            \t\t%s\
            \n\t#3:\
            \t\t%s"\
            % \
                (
                    self.name, self.allotropes, len(self.get_ships()),
                    self.workforce.get_size(), self.workforce.get_free(),
                    self.workforce.get_occupied(), self.workforce.get_disabled(),
                    str(self.planetary),
                    self.get_fleet(0), self.get_fleet(1), self.get_fleet(2)
                )

    def __init__(self, name=None,
            allotropes=0, workforce=12,
            planetary=None, active=True):

        if not name:
            raise PlayerNeedsNameError("Needs name")

        self.name = name
        self.allotropes = allotropes

        self.workforce = Workforce(self, workforce)

        self.planetary = planetary

        self.fleets = [
            fleet.Fleet(owner=self),
            fleet.Fleet(owner=self),
            fleet.Fleet(owner=self)
        ]

        self.display_name = "%s, a stellar commander. Workforce: %d" \
            % (self.name, self.workforce.get_size())

    def get_fleet(self, index):
        return self.fleets[index]

    def get_fleets(self):
        return self.fleets

    def get_planetary(self):
        return self.planetary

    def set_planetary(self, planetary_id):
        assert not self._data_invariant()

        self.planetary = planetary_id

        assert not self._data_invariant()

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
        assert not self._data_invariant()

        self.allotropes = allotropes

        assert not self._data_invariant()

    def add_allotropes(self, amount):
        assert not self._data_invariant()

        if(amount < 0):
            amount = 0

        self.set_allotropes(self.get_allotropes() + amount)

        assert not self._data_invariant()

    def remove_allotropes(self, amount):
        assert not self._data_invariant()

        current_amount = self.get_allotropes()
        diff = current_amount - amount

        if(amount < 0):
            amount = 0

        if(diff < 0):
            amount = current_amount

        self.set_allotropes(self.get_allotropes() - amount)

        assert not self._data_invariant()

    def add_ships(self, ships, fleet_index):
        assert not self._data_invariant()

        self.get_fleet(fleet_index).append_ships(ships)

        assert not self._data_invariant()

    def get_travel_time(self):
        return mission.DEFAULT_TRAVEL_TIME

    def get_ship_total(self):
        total = 0
        for ship in self.get_ships():
            total = total + ship.get_points()

        return total

    def get_allotropes_per_tick(self):
        return len(self.get_ships()) + self.get_workforce().get_size() * 100

    def tick(self, game):
        assert not self._data_invariant()

        #print "Tick on %s" % self.get_display_name()
        for fleet in self.get_fleets():
            mission = fleet.get_mission()
            if(mission):
                if(mission.get_stage() == "completed"):
                    fleet.set_mission(None)

            fleet.tick()

        self.add_allotropes(self.get_allotropes_per_tick())

        assert not self._data_invariant()

    def apply_costs(self, costs, coefficient=1):
        """Loop through costs and apply them individually"""
        withdraw = True

        for cost in costs:
            self.apply_cost(cost, coefficient, withdraw)

        return True

    def is_costs_applicable(self, costs, coefficient=1):
        """Return True if cost is applicable, False if not"""
        applicable = True
        withdraw = False

        for cost in costs:
            try:
                self.apply_cost(cost, coefficient, withdraw)
            except:
                applicable = False

        return applicable

    def apply_cost(self, cost, coefficient, withdraw, revert=False,):
        """Apply a Cost on a Player, raise CostError if the cost cannot be applied"""

        assert not self._data_invariant()

        applied = False

        cost_value = cost.get_multiplied_value(coefficient)
        cost_type = repr(cost)

        if cost_type == 'Workforce Cost':

            if revert:
                self.get_workforce().free_workforce(cost_value)
                return

            if cost_value <= self.get_workforce().get_free():
                if withdraw:
                    self.get_workforce().use_workforce(cost_value)
                applied = True
        elif cost_type == 'Allotrope Cost':

            if revert:
                self.add_allotropes(cost_value)
                return

            if cost_value <= self.get_allotropes():
                applied = True
                if withdraw:
                    self.remove_allotropes(cost_value)

        # cost not applied, let cost raise CostError
        if not applied:
            cost.unsuccessful()

        assert not self._data_invariant()

    def test_criteria(self, criteria):
        """Return True if criteria are satisfied, False if not"""
        met = True

        for criterion in criteria:
            try:
                self.test_criterion(criterion)
            except:
                met = False

        return met

    def test_criterion(self, criterion):
        met = False

        criterion_value = criterion.get_value()
        criterion_type = repr(criterion)

        if criterion_type == 'Stellar Class Criterion':
            if criterion_value <= self.get_planetary().stellar_class:
                met = True

        if not met:
            criterion.unmet()

        return met

    def _data_invariant(self):
        if not __debug__:
            return None

        # name
        if not type(self.name) == type(""):
            raise AssertionError("Player name not a str " % str(self.name))
        elif(self.name == ""):
            raise PlayerNeedsNameError("Player name cannot be an empty string: %s"\
                % str(self.name))

        # allotropes
        if not type(self.allotropes) == type(1):
            raise AssertionError("Allotropes not an int  %s"\
                % str(self.allotropes))
        elif(self.allotropes < 0):
            raise AssertionError("Allotropes is a negative int %s"\
                % str(self.allotropes))

        # planetary
        try:
            self.planetary.get_owner()
        except:
            raise

        # fleets
        try:
            self.fleets[0].get_mission()
        except:
            raise


class PlayerNeedsNameError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
