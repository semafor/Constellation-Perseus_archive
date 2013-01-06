import gameobject
from math import floor
from random import randint


class Ship(gameobject.GameObject):
    def __str__(self):
        """Return string representation of Ship object."""
        return "Ship:\t" + self.name + " (" + self.ship_class + "), hull: " + str(self.hull)

    def __init__(self, name=None, ship_class=1, price=0,

            evade=0, hull=0, counter_measures=None,

            guns=0, guns_warmup_time=0,

            shields=0, shields_restore_time=0):

        self.name = name
        self.ship_class = ship_class

        self.evade = evade
        self.hull = hull
        self.counter_measures = counter_measures
        self.price = price

        # guns
        self.guns = guns
        self._original_guns = guns
        self.guns_warmup_time = guns_warmup_time
        self.guns_states = [0] * self.guns

        self.temp_to_guns = {0: guns}
        """A map from temperature to number of guns of that temperature."""

        # if (name == "Canopus"):
        #     self.guns_states = [55] * guns

        # shields
        self.shields = shields
        self.shields_restore_time = shields_restore_time
        self.current_shields_health = shields

        if ship_class == 0 or ship_class > len(CLASSES):
            raise ShipException("ship_class %s is N/A " % str(ship_class))

        if not price:
            raise ShipException("price cannot be %s" % str(price))

        self.display_name = "%s, a ship, class %d, costing %d" \
            % (self.name, self.ship_class, self.price)

        if __debug__:
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
        if __debug__:
            self.data_invariant()

        self.current_shields_health = health

        if __debug__:
            self.data_invariant()

    def get_shields_health(self):
        return self.current_shields_health

    def reset_shields(self):
        self.set_shields_health(self.get_shields())

    def shields_hit(self):
        """Take a shield hit or hull hit if shields are down.

        Return True if shields took hit, False if hull took hit
        """
        if __debug__:
            self.data_invariant()

        successful_absorb = True

        if(self.get_shields_health() > 0):
            self.set_shields_health(self.get_shields_health() - 1)

        if(self.get_shields_health() == 0):
            self.hull_hit()
            successful_absorb = False

        if __debug__:
            self.data_invariant()

        return successful_absorb

    def shields_restore(self):
        if __debug__:
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

        if __debug__:
            self.data_invariant()

    def get_counter_measures(self):
        return self.counter_measures

    def set_hull(self, hull):
        if __debug__:
            self.data_invariant()

        self.hull = hull

        if __debug__:
            self.data_invariant()

    def get_hull(self):
        return self.hull

    def is_hull_intact(self):
        return self.get_hull() > 0

    def is_gun_warm(self, index):
        """Return True if gun at index is ready to fire"""
        assert not self.data_invariant()

        return self.guns_states[index] >= self.guns_warmup_time

    def hull_hit(self):
        if __debug__:
            self.data_invariant()

        if(self.get_hull > 0):
            self.set_hull(self.get_hull() - 1)

        if __debug__:
            self.data_invariant()

    def get_guns(self):
        """Return number of guns"""
        if __debug__:
            self.data_invariant()
        return self.guns

    def get_warm_guns(self):
        """Return number of warm guns"""
        assert not self.data_invariant()
        warm = 0
        for i in range(self.guns):
            warm = warm + self.is_gun_warm(i)


        dwarm = 0
        if self.guns_warmup_time in self.temp_to_guns:
            dwarm = self.temp_to_guns[self.guns_warmup_time]
        assert warm == dwarm, "get_warm_guns(): warm in list vs warm in dict" + str(warm) + " vs " + str (dwarm)

        assert not self.data_invariant()
        return warm

    def get_class_index(self):
        return self.ship_class

    def get_class_name(self):
        return CLASSES[self.ship_class]["name"]

    def get_guns_states(self):
        return self.guns_states

    def set_gun_state(self, index, state):
        if __debug__:
            self.data_invariant()

        if(type(index) != type(1)):
            raise ValueError("Index not an int: %s" % str(index))

        if(type(state) != type(1)):
            raise ValueError("State not an int: %s" % str(state))


        temp = self.get_gun_state(index)
        if (temp != 0):
            if state in self.temp_to_guns:
                self.temp_to_guns[state] += 1
            else:
                self.temp_to_guns[state] = 1
            self.temp_to_guns[temp] -= 1

        self.guns_states[index] = state

        if __debug__:
            self.data_invariant()

    def get_gun_state(self, index):
        return self.guns_states[index]

    def get_indices_of_warm_guns(self):
        assert not self.data_invariant()
        indices = []
        for i in range(self.guns):
            if (self.is_gun_warm(i)):
                indices.append(i)

        return indices

    def warm_guns(self):
        if __debug__:
            self.data_invariant()
        newdict = {}
        for (k,v) in self.temp_to_guns.items():
            if (k >= self.guns_warmup_time):
                if self.guns_warmup_time in newdict:
                    newdict[self.guns_warmup_time] += v
                else:
                    newdict[self.guns_warmup_time] = v
            else:
                newdict[k+1] = v

        self.temp_to_guns = newdict
        self.guns_states = [min(self.guns_warmup_time, x + 1) for x in self.guns_states]

        if __debug__:
            self.data_invariant()

    def reset_guns(self):
        if __debug__:
            self.data_invariant()

        self.guns_states = [0 for x in self.guns_states]
        self.temp_to_guns = {0 : self.guns}

        if __debug__:
            self.data_invariant()

    def fire_guns(self):
        """Set gun state to 0 if gun is warm"""
        if __debug__:
            self.data_invariant()

        for gun_index in self.get_indices_of_warm_guns():
            self.set_gun_state(gun_index, 0)

        warm_guns = self.temp_to_guns[self.guns_warmup_time]
        self.temp_to_guns[self.guns_warmup_time] = 0
        if (0 in self.temp_to_guns):
            self.temp_to_guns[0] += warm_guns
        else:
            self.temp_to_guns[0] = warm_guns

        if __debug__:
            self.data_invariant()

    def fire_gun(self, gun_index):
        """Set gun index to 0"""
        if __debug__:
            self.data_invariant()

        assert self.guns_states[gun_index] >= self.guns_warmup_time, \
            "Cannot fire cold gun, index=" + str(gun_index) + ", temperature=" + str(self.guns_states[gun_index])

        temp = self.guns_states[gun_index]
        self.guns_states[gun_index] = 0

        # if not absolutely cool
        # add to cold guns
        # subtract this gun from the temperature it was at
        if (temp != 0):
            if 0 in self.temp_to_guns:
                self.temp_to_guns[0] += 1
            else:
                self.temp_to_guns[0] = 1

            self.temp_to_guns[temp] -= 1

        if __debug__:
            self.data_invariant()

    def destroy_random_gun(self):
        if __debug__:
            self.data_invariant()

        available_gun_states = []

        for k, v in self.temp_to_guns.items():
            if (v > 0):
                available_gun_states.append(k)

        gun_to_destroy = randint(0, len(available_gun_states))

        self.set_gun_state(gun_to_destroy, -100)

        # guns_length = self.get_guns() - 1
        # gun = randint(0, guns_length)

        # temp = self.get_gun_state(gun)
        # self.temp_to_guns[temp] -= 1
        # if (-100 in self.temp_to_guns):
        #     self.temp_to_guns[-100] += 1
        # else:
        #     self.temp_to_guns[-100] = 1
        # self.set_gun_state(gun, -100)

        if __debug__:
            self.data_invariant()

    def attack_tick(self):
        if __debug__:
            self.data_invariant()

        # gun warmup
        self.warm_guns()

        # shield tickly restore
        self.shields_restore()

        #print self.dump_data() + "\n"

        if __debug__:
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
            "guns_warmup_time": str(self.guns_warmup_time),
            "current_gun_warmth": str(self.get_guns_states()),

            "shields": str(self.shields),
            "shields_restore_time": str(self.shields_restore_time),
            "current_shields_health": str(self.current_shields_health),
            "attack_points": str(self.get_attack_points()),
            "defence_points": str(self.get_defence_points()),
            "points": str(self.get_points()),
            "hull_intact": str(self.is_hull_intact()),
            "class_name": str(self.get_class_name())
        }

    def data_invariant(self):
        if not __debug__:
            return None

        # counting guns in dict
        gguns = 0
        for (k, v) in self.temp_to_guns.items():
            if (type(v) != type(0)):
                raise AssertionError("Temperature mapped to non-int: %s " % str((k, v)))
            if (v < 0):
                raise AssertionError("Negative number of guns at temperature: %s " % str((k, v)))

            #orig = sum([1 for x in self.guns_states if x == k])
            #assert orig == v, "Error in temperatures, list vs guns, at temperatur = " + str(k) + ": " + str(orig) + " vs " + str(v)

            gguns += v

        assert gguns == self.guns, "Number of guns in dict vs self.guns " + str(gguns) + " != " + str(self.guns)

        wguns = 0
        for (k, v) in self.temp_to_guns.items():
            if k > self.guns_warmup_time and v >= 0:
                raise AssertionError("Guns too warm! " + str((k, v)) + ", when guns_warmup_time = " + str(self.guns_warmup_time))
            if k == self.guns_warmup_time:
                wguns += v

        #wguns_orig = len([x for x in self.guns_states if x >= self.guns_warmup_time])

        #assert wguns == wguns_orig, "Warm guns in dict vs in list: " + str(wguns) + " vs " + str(wguns_orig)

        # print wguns

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

        if(self.guns != self._original_guns):
            raise ValueError("Amount of guns deviates: %s" % str(self.guns))

        # guns warmup
        if(type(self.guns_warmup_time) != type(1)):
            raise ValueError("Warmup %s not an int" % str(self.guns_warmup_time))

        # guns states
        if(type(self.guns_states) != type([])):
            raise ValueError("Guns states %s not an array" % str(self.guns_states))

        if(len(self.guns_states) != self.guns):
            raise ValueError("Gun states length not equal to guns lenght: %s" % str(self.guns_states))

        # guns states
        for state in self.get_guns_states():
            if(state > self.guns_warmup_time):
                raise ValueError("Gun state %s is higher than warmup time %s"\
                    % (str(state), str(self.guns_warmup_time)))

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
        "guns_warmup_time": 2,
        "shields": 50,
        "shields_restore_time": 2
    },
    "beid": {
        "name": "Beid",
        "ship_class": 1,
        "price": 250,
        "hull": 250,
        "guns": 10,
        "guns_warmup_time": 2,
        "shields": 300,
        "shields_restore_time": 3
    },
    "canopus": {
        "name": "Canopus",
        "ship_class": 3,
        "price": 500,
        "hull": 1000,
        "guns": 250,
        "guns_warmup_time": 4,
        "shields": 1000,
        "shields_restore_time": 5
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
