ATWILL = "atwill"
COORDINATED = "coordinated"

DEFENSIVE = "defensive"
AGGRESSIVE = "aggressive"

CLASS = "class"

TOTALGUNS = "totalguns"
CURRENTGUNS = "currentguns"
GUNWARMUP = "gunwarmup"

CLOSETOFIRING = "closetofiring"

TOTALSHIELDS = "totalshields"
CURRENTSHIELDS = "totalshields"
SHIELDRESTORE = "shieldrestore"

HULL = "hull"


class Fleet():
    def __init__(self, owner=None):

        try:
            owner.get_planetary()
        except:
            raise ValueError("Fleet needs owner: %s" % str(owner))

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

        if __debug__:
            self.data_invariant()

    def assign_ships(self, ships):
        if __debug__:
            self.data_invariant()

        if(type(ships) != type([])):
            raise ValueError("Ships need to come as list, not %s" % str(ships))

        self.ships = ships

        if __debug__:
            self.data_invariant()

    def append_ships(self, ships):
        if __debug__:
            self.data_invariant()

        if(type(ships) != type([])):
            raise ValueError("Ships need to come as list, not %s" % str(ships))

        self.ships = self.ships + ships

        self.get_ships_ordered_by(TOTALSHIELDS)

        if __debug__:
            self.data_invariant()

    def remove_ship(self, ship):
        if __debug__:
            self.data_invariant()

        self.ships.remove(ship)

        if __debug__:
            self.data_invariant()

    def set_mission(self, mission):
        if __debug__:
            self.data_invariant()

        self.mission = mission

        if __debug__:
            self.data_invariant()

    def get_mission(self):
        return self.mission

    def abort_mission(self):
        if(self.get_mission()):
            self.get_mission().abort()

    def get_raw_ships(self):
        return self.ships

    def get_ships(self):
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
        result = []

        if(criterion == CLASS):
            result = sorted(self.get_ships(), key=lambda ship: ship.get_class_index(), reverse=reverse)

        elif(criterion == HULL):
            result = sorted(self.get_ships(), key=lambda ship: ship.get_hull(), reverse=reverse)

        elif(criterion == CURRENTGUNS):
            result = sorted(self.get_ships(), key=lambda ship: ship.get_amount_of_warm_guns(), reverse=reverse)
        elif(criterion == TOTALGUNS):
            result = sorted(self.get_ships(), key=lambda ship: ship.guns, reverse=reverse)
        elif(criterion == GUNWARMUP):
            result = sorted(self.get_ships(), key=lambda ship: ship.guns_warmup_time, reverse=reverse)

        elif(criterion == CLOSETOFIRING):
            warm_guns = [gun for gun in self.get_ships() if True] # TODO fix conditional in comprehension
            result = sorted(self.get_ships(), key=lambda ship: ship.get_amount_of_warm_guns, reverse=reverse)
            result = sorted(self.get_ships(), key=lambda ship: ship.guns_warmup_time, reverse=reverse)


        elif(criterion == CURRENTSHIELDS):
            result = sorted(self.get_ships(), key=lambda ship: ship.get_shields_health(), reverse=reverse)
        elif(criterion == TOTALSHIELDS):
            result = sorted(self.get_ships(), key=lambda ship: ship.get_shields(), reverse=reverse)
        elif(criterion == SHIELDRESTORE):
            result = sorted(self.get_ships(), key=lambda ship: ship.shields_restore_time, reverse=reverse)

        # for s in result:
        #     print "Hull: %s" % str(s.get_hull())
        #     print "Total guns: %s" % str(s.guns)
        #     print "Warm guns: %s" % str(s.get_amount_of_warm_guns())
        #     print "Total shields: %s" % str(s.get_shields())
        #     print "Current shields: %s" % str(s.get_shields_health())
        #     print "Gun warmup time: %s" % str(s.guns_warmup_time)
        #     print "Shield restore time: %s" % str(s.shields_restore_time)
        #     print "Class: %s" % str(s.get_name())
        #     print "\n"

        return result

    def get_owner(self):
        return self.owner

    def set_coordination_mode(self, mode):
        if __debug__:
            self.data_invariant()

        self.coordination_mode = mode

        if __debug__:
            self.data_invariant()

    def get_coordination_mode(self):
        return self.coordination_mode

    def set_attack_mode(self, mode):
        if __debug__:
            self.data_invariant()

        self.attack_mode = mode

        if __debug__:
            self.data_invariant()

    def get_attack_mode(self):
        return self.attack_mode

    def tick(self):
        if __debug__:
            self.data_invariant()

        if(self.mission):
            self.mission.tick()

        if __debug__:
            self.data_invariant()

    def data_invariant(self):
        if not __debug__:
            return None

        if(type(self.ships) != type([])):
            raise ValueError("Ships not a list %s" % str(self.ships))

        if(self.get_mission()):
            mission = self.get_mission()
            try:
                mission.get_stage()
            except:
                raise FleetException("Bad fleet mission %s"\
                    % str(mission.get_stage()))

        if(self.coordination_mode != ATWILL and self.coordination_mode != COORDINATED):
            raise ValueError("coordination_mode not valid: %s" % str(self.coordination_mode))

        if(self.attack_mode != AGGRESSIVE and self.attack_mode != DEFENSIVE):
            raise ValueError("attack_mode not valid: %s" % str(self.attack_mode))


class FleetException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
