ATWILL = "atwill"
TIMED = "timed"
TIMEDTHRESHOLD = 90  # how many percent of guns must be warm before firing


DEFENSIVE = "defensive"
AGGRESSIVE = "aggressive"

CLASS = "class"

TOTALGUNS = "totalguns"
CURRENTGUNS = "currentguns"
GUNWARMUP = "gunwarmup"

CLOSETOFIRING = "closetofiring"
CLOSETODESTRUCT = "closetodestruct"

TOTALSHIELDS = "totalshields"
CURRENTSHIELDS = "totalshields"
SHIELDRESTORE = "shieldrestore"

HULL = "hull"


class Fleet():
    """Represents a list of ships.

        - Fleet can be on a Mission
        - If fleet is in a Attack which fires on Planetary Shields, it is given resources
            which in turn is passed on to the mission

    """
    def __str__(self):

        ships_of_type = {}

        for n, ship in enumerate(self.get_ships()):
            t = ship.get_name().lower()

            try:
                ships_of_type[t]
            except:
                ships_of_type[t] = 0

            ships_of_type[t] = ships_of_type[t] + 1

        return "\
            \n\tShips:\t\t%d\
            \n\tShip types:\t%s\
            \n\tMission:\t%s\n\
            "\
                % (\
                    len(self.get_ships()),
                    str(ships_of_type),
                    str(self.get_mission())
                )

    def __repr__(self):
        return "Fleet"

    def __init__(self, owner=None):

        self.owner = owner
        self.ships = []
        self.mission = None

        # "At will" or "Blast"
        self.coordination_mode = ATWILL
        """The coordination_mode variable denotes how the ships in a fleet will attack.  In "At will" mode, every gun is fired
        when ready.  In the "Blast" mode, every ship waits til a great deal (maximum five ticks) of guns are warm and then fire simultaneously.  The
        "Blast" mode is more risky but effective as it can take out shields and hull in one go, effectively wiping out more ships."""

        # "Defensive" or "Aggressive"
        self.attack_mode = DEFENSIVE
        """The two attack modes are "Defensive" and "Aggressive".  In the "Defensive" mode, the fleet will try to take out ships
        that poses an immediate threat to the fleet, not necessarily trying to kill the most number of enemy ships. The other
        mode, "Aggressive", aims to maximize the number of killed enemy ships.  Every ship in the fleet will try to take out a
        ship if its shields are down or hull damaged.  The "Defensive" mode is a good defending strategy."""

        assert not self.data_invariant()

    def assign_ships(self, ships):
        assert not self.data_invariant()

        if(type(ships) != type([])):
            raise ValueError("Ships need to come as list, not %s" % str(ships))

        self.ships = []

        for ship in ships:
            self.add_ship(ship)

        assert not self.data_invariant()

    def append_ships(self, ships):
        assert not self.data_invariant()

        if(type(ships) != type([])):
            raise ValueError("Ships need to come as list, not %s" % str(ships))

        for ship in ships:
            self.add_ship(ship)

        assert not self.data_invariant()

    def add_ship(self, ship):
        assert not self.data_invariant()

        ship._fleet = self
        self.ships.append(ship)

        assert not self.data_invariant()

    def remove_ship(self, ship):

        self.ships.remove(ship)

        assert not self.data_invariant()

    def set_mission(self, mission):
        assert not self.data_invariant()

        self.mission = mission

        assert not self.data_invariant()

    def get_mission(self):
        return self.mission

    def abort_mission(self):
        if(self.get_mission()):
            self.get_mission().abort()

    def get_ships(self):
        for ship in self.ships:
            if not ship.is_hull_intact():
                raise FleetException("Broken ship still in fleet")

        return self.ships

    def get_guns(self):
        """Return number of guns in fleet"""
        guns = 0

        for ship in self.get_ships():
            guns = guns + ship.guns

        return guns

    def get_warm_guns(self):
        """Return number of warm guns in fleet"""
        warm = 0

        for ship in self.get_ships():
            warm += ship.get_warm_guns()

        return warm

    def get_ships_ordered_by(self, criterion, reverse=False):
        """Return ships in fleet ordered by criterion, ascending by default"""

        result = []

        # class
        if(criterion == CLASS):
            result = sorted(self.get_ships(), key=lambda ship: ship.get_class_index(), reverse=reverse)

        # hull
        elif(criterion == HULL):
            result = sorted(self.get_ships(), key=lambda ship: ship.get_hull(), reverse=reverse)

        # guns
        elif(criterion == CURRENTGUNS):
            result = sorted(self.get_ships(), key=lambda ship: ship.get_warm_guns(), reverse=reverse)
        elif(criterion == TOTALGUNS):
            result = sorted(self.get_ships(), key=lambda ship: ship.guns, reverse=reverse)
        elif(criterion == GUNWARMUP):
            result = sorted(self.get_ships(), key=lambda ship: ship.guns_warm_temperature, reverse=reverse)

        # composite
        elif(criterion == CLOSETOFIRING):
            result = sorted(self.get_ships(), key=lambda ship: (-ship.get_warm_guns(), ship.guns_warm_temperature))
        elif(criterion == CLOSETODESTRUCT):
            result = sorted(self.get_ships(), key=lambda ship: (ship.get_hull(), ship.get_shields_health()))

        # shields
        elif(criterion == CURRENTSHIELDS):
            result = sorted(self.get_ships(), key=lambda ship: ship.get_shields_health(), reverse=reverse)
        elif(criterion == TOTALSHIELDS):
            result = sorted(self.get_ships(), key=lambda ship: ship.get_shields(), reverse=reverse)
        elif(criterion == SHIELDRESTORE):
            result = sorted(self.get_ships(), key=lambda ship: ship.shields_restore_time, reverse=reverse)

        return result

    def get_owner(self):
        return self.owner

    def set_coordination_mode(self, mode):
        assert not self.data_invariant()

        self.coordination_mode = mode

        assert not self.data_invariant()

    def get_coordination_mode(self):
        return self.coordination_mode

    def set_attack_mode(self, mode):
        assert not self.data_invariant()

        self.attack_mode = mode

        assert not self.data_invariant()

    def get_attack_mode(self):
        return self.attack_mode

    def tick(self):
        assert not self.data_invariant()

        if(self.mission):
            self.mission.tick()

        assert not self.data_invariant()

    def data_invariant(self):
        if not __debug__:
            return None

        if(type(self.ships) != type([])):
            raise AssertionError("Ships not a list %s" % str(self.ships))

        try:
            self.get_owner().get_planetary()
        except:
            raise

        # check ships in fleet
        # for ship in self.ships:
        #     if not ship._fleet == self:
        #         raise FleetException("Ship %s _fleet field not this fleet" % ship)

        #     if not ship.is_hull_intact():
        #         raise FleetException("Ship %s is broken" % ship)

        #     if(self.ships.count(ship) > 1):
        #         raise FleetException("Ship %s appears more than once in fleet: %d" % (str(ship), self.ships.count(ship)))

        if(self.get_mission()):
            mission = self.get_mission()
            try:
                mission.get_stage()
            except:
                raise

        if(self.coordination_mode != ATWILL and self.coordination_mode != TIMED):
            raise AssertionError("coordination_mode not valid: %s" % str(self.coordination_mode))

        if(self.attack_mode != AGGRESSIVE and self.attack_mode != DEFENSIVE):
            raise AssertionError("attack_mode not valid: %s" % str(self.attack_mode))
