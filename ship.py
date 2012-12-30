import gameobject
from math import floor


class Ship(gameobject.GameObject):
    def __init__(self, name=None, ship_class=1, price=0,

            evade=0, hull=0, counter_measures=None,

            guns=0, gun_warmup=0,

            shields=0, shields_restore_time=0):

        self.name = name
        self.ship_class = ship_class

        self.evade = evade
        self.hull = hull
        self.counter_measures = counter_measures
        self.price = price

        # guns
        self.guns = guns
        self.gun_warmup = gun_warmup
        self.current_gun_warmth = 0

        # shields
        self.shields = shields
        self.shields_restore_time = shields_restore_time
        self.current_shields_health = shields

        # data
        self.data = {
            "guns_shots": 0,
            "guns_missed_shots": 0,
            "battle_waves": 0,
            "shields_hits": 0,
            "hull_hits": 0,
        }

        if ship_class == 0 or ship_class > len(CLASSES):
            raise ShipException("ship_class %s is N/A " % str(ship_class))

        if not price:
            raise ShipException("price cannot be %s" % str(price))

        self.display_name = "%s, a ship, class %d, costing %d" \
            % (self.name, self.ship_class, self.price)

        self.data_invariant()

    def get_attack_points(self):
        points = 1

        # add guns
        points = points + self.get_guns()

        # add intimidation
        points = points + self.get_intimidation()

        # multiply by index
        points = points * self.get_class_index()

        return points

    def get_defence_points(self):
        points = 1

        # add shields
        points = points + self.get_shields()

        # has counter measures
        if self.counter_measures:
            points = points + 10

        # multiply by index
        points = points * self.get_class_index()

        # subtract hull
        points = (points / 100) * self.get_hull()

        return points

    def get_points(self):
        return self.get_defence_points() + self.get_attack_points()

    def get_intimidation(self):
        return self.get_class_index() * 10

    def get_price(self):
        return self.price

    def get_shields(self):
        return self.shields

    def set_shields_health(self, health):
        self.data_invariant()

        self.current_shields_health = health

        self.data_invariant()

    def get_shields_health(self):
        return self.current_shields_health

    def reset_shields(self):
        self.set_shields_health(self.get_shields())

    def shields_hit(self):
        """Take a shield hit or hull hit if shields are down.

        Return True if shields took hit, False if hull took hit
        """
        self.data_invariant()

        successful_absorb = True

        if(self.get_shields_health() > 0):
            self.set_shields_health(self.get_shields_health() - 1)

        if(self.get_shields_health() == 0):
            self.hull_hit()
            successful_absorb = False

        self.data["shields_hits"] = self.data["shields_hits"] + 1

        self.data_invariant()

        return successful_absorb

    def shields_restore(self):
        self.data_invariant()

        tickly_restore_value =\
            int(floor(self.shields / self.shields_restore_time))

        if((tickly_restore_value + self.get_shields_health())\
            > self.shields):
            # set to orignal value
            self.set_shields_health(self.get_shields())
        else:
            self.set_shields_health(self.get_shields_health()\
                + tickly_restore_value)

        self.data_invariant()

    def get_counter_measures(self):
        return self.counter_measures

    def set_hull(self, hull):
        self.data_invariant()

        self.hull = hull

        self.data_invariant()

    def get_hull(self):
        return self.hull

    def is_hull_intact(self):
        return self.get_hull() > 0

    def hull_hit(self):
        self.data_invariant()

        if(self.get_hull > 0):
            self.set_hull(self.get_hull() - 1)

        self.data["hull_hits"] = self.data["hull_hits"] + 1

        self.data_invariant()

    def get_guns(self):
        return self.guns

    def get_class_index(self):
        return self.ship_class

    def get_class_name(self):
        return CLASSES[self.ship_class]["name"]

    def get_gun_warmth(self):
        return self.current_gun_warmth

    def is_guns_warm(self):
        return (self.gun_warmup == self.current_gun_warmth)

    def set_gun_warmth(self, gun_warmth):
        self.data_invariant()

        self.current_gun_warmth = gun_warmth

        self.data_invariant()

    def guns_fire(self):
        self.data_invariant()

        self.data["guns_shots"] = self.data["guns_shots"] + 1
        self.set_gun_warmth(0)

        self.data_invariant()

    def attack_tick(self):
        self.data_invariant()

        self.data["battle_waves"] = self.data["battle_waves"] + 1

        # gun warmup
        if(self.get_gun_warmth() < self.gun_warmup):
            self.set_gun_warmth(self.get_gun_warmth() + 1)

        # shield tickly restore
        self.shields_restore()

        self.data_invariant()

    def dump_data(self):
        return {
            "name": str(self.name),
            "ship_class": str(self.ship_class),

            "evade": str(self.evade),
            "hull": str(self.hull),
            "counter_measures": str(self.counter_measures),
            "price": str(self.price),

            "guns": str(self.guns),
            "gun_warmup": str(self.gun_warmup),
            "current_gun_warmth": str(self.current_gun_warmth),

            "shields": str(self.shields),
            "shields_restore_time": str(self.shields_restore_time),
            "current_shields_health": str(self.current_shields_health),
            "attack_points": str(self.get_attack_points()),
            "defence_points": str(self.get_defence_points()),
            "points": str(self.get_points()),
            "hull_intact": str(self.is_hull_intact()),
            "class_name": str(self.get_class_name()),
            "guns_warm": str(self.is_guns_warm()),
            "ship_totals": self.data
        }

    def data_invariant(self):

        if(type(self.name) != type("")):
            raise ValueError("Name %s not a string" % str(self.name))

        if(type(self.ship_class) != type(1)):
            raise ValueError("Ship class %s not an int" % str(self.ship_class))

        if(type(self.evade) != type(1)):
            raise ValueError("Evade %s not an int" % str(self.evade))

        # hull
        if(type(self.hull) != type(1)):
            raise ValueError("Hull %s not an int" % str(self.hull))

        if(self.hull < 0):
            raise ValueError("Hull lt 0: %s" % str(self.hull))

        # price
        if(type(self.price) != type(1)):
            raise ValueError("Price %s not an int" % str(self.price))

        # guns
        if(type(self.guns) != type(1)):
            raise ValueError("Guns %s not an int" % str(self.guns))

        # guns warmup
        if(type(self.gun_warmup) != type(1)):
            raise ValueError("Warmup %s not an int" % str(self.gun_warmup))
        if(type(self.current_gun_warmth) != type(1)):
            raise ValueError("Current gun warmth %s not an int"\
                % str(self.current_gun_warmth))
        if(self.gun_warmup < self.current_gun_warmth):
            raise ValueError("Current gun warmth %s warmer than warm"\
                % str(self.current_gun_warmth))
        if(self.gun_warmup % 2 != 0):
            raise ValueError("Gun warmup needs to be an even int")

        # shields
        if(type(self.shields) != type(1)):
            raise ValueError("Shields %s not an int" % str(self.shields))

        # shields restore
        if(type(self.current_shields_health) != type(1)):
            raise ValueError("Current shield health %s not an int"\
                % str(self.current_shields_health))
        if(self.shields < self.current_shields_health):
            raise ValueError("Current shield health %s is too high"\
                % str(self.current_shields_health))

        if(self.shields_restore_time < 1):
            raise ValueError("shields_restore_time less than 1: %s"\
                % str(self.shields_restore_time))

TYPES = {
    # name, class, price, hull, guns, shields
    "ain": {
        "name": "Ain",
        "ship_class": 1,
        "price": 100,
        "hull": 150,
        "guns": 5,
        "gun_warmup": 2,
        "shields": 100,
        "shields_restore_time": 3
    },
    "beid": {
        "name": "Beid",
        "ship_class": 1,
        "price": 250,
        "hull": 250,
        "guns": 10,
        "gun_warmup": 2,
        "shields": 300,
        "shields_restore_time": 3
    }
}

CLASSES = [
    None,
    {
        "name": "Fighter",
        "description": "",
    },
    {
        "name": "Cruiser",
        "description": "",
    },
    {
        "name": "Destroyer",
        "description": "",
    },
    {
        "name": "Dreadnaught",
        "description": "",
    },
    {
        "name": "Galactic Supernaught",
        "description": "",
    },
]


class ShipException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
