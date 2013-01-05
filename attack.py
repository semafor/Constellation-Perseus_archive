from random import randint
from fleet import DEFENSIVE, AGGRESSIVE, CURRENTSHIELDS, CLOSETOFIRING, CLOSETODESTRUCT

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

            # defenders shooting first
            self.force_vs_force(self.defending_force,\
                self.attacking_force, 5)
            self.force_vs_force(self.attacking_force,\
                self.defending_force, 35)

            # run attack tick on all fleets
            for ship in self.all_ships:
                ship.attack_tick()

        self.complete()

    def complete(self):
        for ship in self.all_ships:
            ship.reset_guns()
            ship.reset_shields()

    def force_vs_force(self, attacking_force, defending_force, miss_chance):

        defending_ships = []

        # cycle through attacking fleets and execute their desired attack
        for fleet in attacking_force.get_fleets():

            attack_mode = fleet.get_attack_mode()

            # get warm attacking guns
            attacking_guns = fleet.get_warm_guns()

            if(attacking_guns):

                # fetch ships in desired order
                if(attack_mode == DEFENSIVE):
                    defending_ships = defending_force.get_all_ships_ordered(CLOSETOFIRING)
                elif(attack_mode == AGGRESSIVE):
                    defending_ships = defending_force.get_all_ships_ordered(CLOSETODESTRUCT)

                for ship in defending_ships:
                    while(ship.is_hull_intact() and attacking_guns):

                        # decrease amount of guns
                        attacking_guns = attacking_guns - 1

                        # specified misfire, stop firing
                        if(self.get_possibility(miss_chance)):
                            continue

                        # natural misfire, stop firing from this gun
                        if(self.get_natural_misfire()):
                            continue

                        # hit shields, if healthy, hull if not
                        ship.shields_hit()

                        # critical hit destroys ship
                        if(self.get_critical_hit()):
                            if randint(0, 1):
                                ship.set_hull(0)
                            else:
                                ship.destroy_random_gun()

                    if not ship.is_hull_intact():
                        ship._fleet.remove_ship(ship)
                        ship._fleet.get_owner().remove_ship(ship)
                        continue

                    # guns were depleted
                    if(attacking_guns == 0):
                        break

        # if(attacking_force_guns):
        #     for ship in defending_force.get_all_ships():
        #         while(ship.is_hull_intact() and attacking_force_guns):

        #             attacking_force_guns = attacking_force_guns - 1

        #             self.gun_vs_ship(ship)

        #         # ship was destroyed, remove from fleet
        #         if not ship.is_hull_intact():
        #             ship._fleet.remove_ship(ship)
        #             ship._fleet.get_owner().remove_ship(ship)
        #             continue

        #         # guns were depleted
        #         if(attacking_force_guns == 0):
        #             break

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
