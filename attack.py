from random import randint
from fleet import DEFENSIVE, AGGRESSIVE,\
        CLOSETOFIRING, CLOSETODESTRUCT,\
        ATWILL, TIMED, TIMEDTHRESHOLD

ATTACK_TICKS = 10

CRITICAL_HIT = 1
NATURAL_MISFIRE = 5


class Attack():
    """Class that lets one force attack another"""
    def __init__(self, attacking_force, defending_force, location):
        self.attack_tick = 0

        self.location = location

        self.attacking_force = attacking_force
        self.defending_force = defending_force

        self.all_ships = self.attacking_force.get_all_ships()\
            + self.defending_force.get_all_ships()

        assert not self.data_invariant()

        for n, tick in enumerate(range(ATTACK_TICKS)):

            # only attack if defenders
            if len(defending_force.get_all_ships()):

                # defenders shooting first
                self.force_vs_force(self.defending_force,\
                    self.attacking_force, 5)
                self.force_vs_force(self.attacking_force,\
                    self.defending_force, 35)

            # run attack tick on all fleets
            for ship in self.all_ships:
                ship.attack_tick()

            assert not self.data_invariant()

        assert not self.data_invariant()

    def force_vs_force(self, attacking_force, defending_force, miss_chance):
        """Cycle through attacking ships and fire guns at defending ships"""
        # cycle through attacking fleets and execute their desired attack
        for attacking_fleet in attacking_force.get_fleets():

            if(attacking_fleet.get_warm_guns() <= 0):
                continue

            attack_mode = attacking_fleet.get_attack_mode()
            coordination_mode = attacking_fleet.get_coordination_mode()

            attacking_ships = attacking_fleet.get_ships()
            defending_ships = []

            # fetch ships in desired order
            if(attack_mode == DEFENSIVE):
                defending_ships = defending_force.get_all_ships_ordered(CLOSETOFIRING)
            elif(attack_mode == AGGRESSIVE):
                defending_ships = defending_force.get_all_ships_ordered(CLOSETODESTRUCT)

            # if timed attack, wait until TIMEDTHRESHOLD of guns are warm
            if(coordination_mode == TIMED):
                total_guns = attacking_fleet.get_guns()
                warm_guns = attacking_fleet.get_warm_guns()

                percentage_warm = warm_guns / (total_guns / 100)

                if(round(percentage_warm) < TIMEDTHRESHOLD):
                    continue

            for attacking_ship in attacking_ships:

                while(attacking_ship.get_warm_guns() > 0 and len(defending_ships) > 0):

                    defending_ship = defending_ships[0]

                    attacking_ship.fire_gun()

                    # attack/defence misfire
                    if(randint(1, 100) <= miss_chance):
                        continue

                    # natural misfire
                    if(randint(1, 100) <= NATURAL_MISFIRE):
                        continue

                    # critical hit destroys ship
                    if(self.get_critical_hit()):
                        if randint(0, 1):
                            if(defending_ship.is_hull_intact()):
                                defending_ship.set_hull(0)
                        else:
                            defending_ship.destroy_random_gun()

                    if not defending_ship.is_hull_intact():
                        defending_ships.pop(0)
                        continue

                    # actual ship hit
                    defending_ship.shields_hit()

    def get_critical_hit(self):
        """Return True if the random number was less than CRITICAL_HIT"""
        return randint(1, 1000) <= CRITICAL_HIT

    def data_invariant(self):
        if not __debug__:
            return None

        try:
            self.attacking_force.get_fleets()
        except:
            raise ForceError("Attacking force not a Force: %s"\
                % str(self.attacking_force))

        try:
            self.defending_force.get_fleets()
        except:
            raise ForceError("Defending force a Force: %s"\
                % str(self.defending_force))

        try:
            self.location.get_friendly_fleets()
        except:
            raise LocationError("Location not a planetary: %s"\
                % str(self.location))

        for fleet in self.attacking_force.get_fleets():
            if self.defending_force.get_fleets().count(fleet):
                raise FleetBothAttackerAndDefenderError("Attacking fleet %s is also defending" % str(fleet))


class ForceError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class LocationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class FleetBothAttackerAndDefenderError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
