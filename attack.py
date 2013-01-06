from random import randint
from fleet import DEFENSIVE, AGGRESSIVE,\
        CLOSETOFIRING, CLOSETODESTRUCT,\
        ATWILL, TIMED, TIMEDTHRESHOLD

ATTACK_TICKS = 10

CRITICAL_HIT = 1
NATURAL_MISFIRE = 5


class Attack():
    def __init__(self, attacking_force, defending_force):
        self.attack_tick = 0

        try:
            attacking_force.get_fleets()
        except:
            raise AttackException("Attacking force not a Force: %s"\
                % str(attacking_force))

        try:
            defending_force.get_fleets()
        except:
            raise AttackException("Defending force a Force: %s"\
                % str(defending_force))

        self.attacking_force = attacking_force
        self.defending_force = defending_force

        self.all_ships = self.attacking_force.get_all_ships()\
            + self.defending_force.get_all_ships()

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

    def force_vs_force(self, attacking_force, defending_force, miss_chance):

        # cycle through attacking fleets and execute their desired attack
        for attacking_fleet in attacking_force.get_fleets():

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

                # no more defenders
                if(len(defending_ships) == 0):
                    break

                for defending_ship in defending_ships:

                    for gun in range(attacking_ship.get_warm_guns()):

                        if not defending_ship.is_hull_intact():
                            # if ship is destroyed, remove ship from all it's parent lists
                            # TODO: ship should be able to be removed from everywhere in one command (.destroy() on ship?)
                            continue

                        attacking_ship.fire_gun()

                        # specified misfire, stop firing
                        if(self.get_possibility(miss_chance)):
                            continue

                        # natural misfire, stop firing from this gun
                        if(self.get_natural_misfire()):
                            continue

                        # hit shields, if healthy, hull if not
                        defending_ship.shields_hit()

                        # critical hit destroys ship
                        if(self.get_critical_hit()):
                            if randint(0, 1):
                                defending_ship.set_hull(0)
                            else:
                                defending_ship.destroy_random_gun()

                        if not defending_ship.is_hull_intact():
                            # if ship is destroyed, remove ship from all it's parent lists
                            # TODO: ship should be able to be removed from everywhere in one command (.destroy() on ship?)
                            defending_ship._fleet.remove_ship(defending_ship)
                            defending_ship._fleet.get_owner().remove_ship(defending_ship)
                            defending_ships.remove(defending_ship)
                            continue

    def get_possibility(self, percentage):
        return randint(1, 100) <= percentage

    def get_critical_hit(self):
        return randint(1, 1000) <= CRITICAL_HIT

    def get_natural_misfire(self):
        return self.get_possibility(NATURAL_MISFIRE)


class AttackException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
