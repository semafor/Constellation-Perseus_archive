ATTACK_TICKS = 10


class Attack():
    def __init__(self, attacking_fleets, defending_fleets):

        self.attack_tick = 0

        try:
            for fleet in attacking_fleets:
                fleet.get_mission()
        except:
            raise AttackException("Attacking fleets not list of fleets: %s"\
                % str(attacking_fleets))

        try:
            for fleet in defending_fleets:
                fleet.get_mission()
        except:
            raise AttackException("Defending fleets not list of fleets: %s"\
                % str(defending_fleets))

        self.remove_empty_fleets(attacking_fleets)
        self.remove_empty_fleets(defending_fleets)

        self.attacking_fleets = attacking_fleets
        self.defending_fleets = defending_fleets

        self.all_fleets = self.attacking_fleets + self.defending_fleets

        for n, tick in enumerate(range(ATTACK_TICKS)):

            # run attack tick on all fleets
            for ship in self.get_all_ships_from_fleets(self.all_fleets):
                ship.attack_tick()

            # defenders shooting first
            self.fleets_attack_fleets(self.defending_fleets,\
                self.attacking_fleets)
            self.fleets_attack_fleets(self.attacking_fleets,\
                self.defending_fleets)

        self.complete()

    def complete(self):
        for ship in self.get_all_ships_from_fleets(self.all_fleets):
            ship.set_gun_warmth(0)
            ship.reset_shields()

    def get_fired_guns(self, fleets):
        guns = 0
        for ship in self.get_all_ships_from_fleets(fleets):
            if(ship.is_guns_warm() and ship.is_hull_intact()):
                guns = guns + ship.get_guns()
                ship.guns_fire()

        return guns

    def get_all_ships_from_fleets(self, fleets):
        ships = []
        for fleet in fleets:
            for ship in fleet.get_ships():
                ships.append(ship)
                ship._fleet = fleet

        return ships

    def fleets_attack_fleets(self, attacking_fleets, defending_fleets):

        attacking_fleets_guns = self.get_fired_guns(attacking_fleets)

        for ship in self.get_all_ships_from_fleets(defending_fleets):
            while(ship.is_hull_intact() and attacking_fleets_guns):
                ship.shields_hit()

                attacking_fleets_guns = attacking_fleets_guns - 1

            if not ship.is_hull_intact():
                ship._destroyed = True
                ship._fleet.remove_ship(ship)

            if(attacking_fleets_guns == 0):
                break

    def remove_empty_fleets(self, list_of_fleets):
        for index, fleet in enumerate(list_of_fleets[:]):
            if(len(fleet.get_ships()) == 0):
                list_of_fleets.remove(fleet)


class AttackException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
