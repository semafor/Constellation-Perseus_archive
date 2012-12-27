import uuid
import mission


class Game():
    def __init__(self):
        self.game_object_by_uuid = {}
        self.game_object_by_game_object = {}
        self.player_by_name = {}
        self.tick = Tick()

    def create(self, what, **kwargs):
        """Return a GameObject.

        Keyword arguments:
        what -- the GameObject class (default GameObject)
        args -- arguments to pass on to the GameObject class
        """

        if not what:
            raise GameException("cannot create %s " % str(what))

        game_object = what(**kwargs)

        # by uid
        game_object_uuid = str(uuid.uuid4())[:5]
        game_object.set_id(game_object_uuid)
        self.game_object_by_uuid[game_object_uuid] = game_object

        # by game_object
        self.game_object_by_game_object[game_object] = game_object_uuid

        return game_object

    def create_player(self, name, **kwargs):
        """Return None if name is empty or already existing username else create a player object and return it."""
        if ((type("")) != type(name)):
            name = str(name)
        name = name.strip()
        if (len(name) == 0):
            return None
        if name in self.player_by_name:
            # duplicate username
            return None

        kwargs["name"] = name

        player = self.create(Player, **kwargs)

        self.player_by_name[name] = player

        return player

    def create_planetary(self, **kwargs):
        return self.create(Planetary, **kwargs)

    def create_ship(self, **kwargs):
        return self.create(Ship, **kwargs)

    def get_available_ships(self):
        return {
            "ain": {
                "price": 100,
                "ship_class": 1,
                "name": "Ain",
            },
            "beid": {
                "price": 200,
                "ship_class": 1,
                "name": "Beid",
            }
        }

    def buy_ships(self, player, ship_enum, amount, fleet_index=0):
        """Return False iff not enough allotropes.

        Keyword arguments:
        """
        available_ships = self.get_available_ships()
        ships = []

        if not ship_enum:
            raise ValueError("cannot buy ship of %s type" % str(ship_enum))

        if not player:
            raise ValueError("player cannot be %s " % str(player))

        if not type(amount) == type(1):
            raise ValueError("amount must be an int: %s" % str(amount))

        if amount < 0:
            raise ValueError("amount must not be negative: %s" % str(amount))

        try:
            available_ships[ship_enum]
        except:
            return False

        total_amount = available_ships[ship_enum]["price"] * amount

        player_allotropes = player.get_allotropes()

        #print "total_amount %d, player_allotropes %d" % (int(total_amount), int(player_allotropes))

        # check if player can afford it
        if (total_amount > player_allotropes):
            return False

        for i in range(amount):
            s = self.create_ship(**available_ships[ship_enum])

            ships.append(s)

        # subtract allotropes
        player.set_allotropes(player_allotropes - total_amount)

        player.add_ships(ships, fleet_index)

        return True

    def attack(self, attacking_player, defending_player, fleet_index, target_stay):
        if(type(attacking_player) != type(Player(name="x"))):
            raise ValueError("Attacking player needs to be Player, not %s" % str(attacking_player))

        if(type(defending_player) != type(Player(name="x"))):
            raise ValueError("Defending player needs to be Player, not %s" % str(defending_player))

        if(type(fleet_index) != type(1)):
            raise ValueError("Attacker must specify fleet, other than %s" % str(fleet_index))

        if(type(target_stay) != type(1)):
            raise ValueError("Specify for how long attack will last, not %s" % str(target_stay))

        if(len(attacking_player.get_fleet(fleet_index).get_ships()) == 0):
            raise GameException("Attacking player have no ships in fleet %d" % fleet_index)
            return False

        #player, target, mission_type, target_stay):
        fleet = attacking_player.get_fleet(fleet_index)
        m = mission.Mission(attacking_player, defending_player, mission.ATTACK, target_stay)
        fleet.set_mission(m)

        return m

    def get_by_id(self, thing_id):
        return self.game_object_by_uuid[thing_id]

    def get_by_obj(self, obj):
        return self.game_object_by_game_object[obj]

    def get_by_name(self, name, case=False):
        results = []
        for obj in self.game_object_by_game_object:
            # case insensitive
            if not case:
                if(name.lower() == obj.get_name().lower()):
                    results.append(obj)
            # case sensitive
            else:
                if(name == obj.get_name()):
                    results.append(obj)

        return results

    def get_all_id(self):
        return self.game_object_by_uuid

    def get_all_gameobjects(self):
        return self.game_object_by_game_object

    def next_tick(self):
        """Add one to tick and run tick on GameObjects"""
        self.tick.next()

        for obj in self.get_all_gameobjects():
            obj.tick()

    def get_current_tick(self):
        """Return current tick"""
        return self.tick.get_tick()


class GameObject():
    def get_display_name(self):
        """Return display name."""
        return self.display_name

    def get_name(self):
        """Return name."""
        return self.name

    def set_active(self):
        """Make active True."""
        self.active = True

    def set_inactive(self):
        """Make active False."""
        self.active = False

    def get_active(self):
        """Return active."""
        return self.active

    def get_id(self):
        return self.uuid

    def set_id(self, _uuid):
        self.uuid = _uuid

    def tick(self):
        """Do nothing."""
        pass


class Tick():
    def __init__(self, genesis=0):
        self.current_tick = genesis

    def next(self):
        """Add one to tick."""
        self.current_tick = self.current_tick + 1

    def get_tick(self):
        """Return current tick."""
        return self.current_tick


class Player(GameObject):
    def __init__(self, name=None,
            allotropes=None, ships=None, workforce=12,
            planetary=None, active=True):

        if not name:
            raise PlayersException("Needs name")

        self.name = name
        self.allotropes = allotropes
        self.ships = ships
        self.workforce = workforce
        self.planetary = planetary

        self.ships = []

        self.fleets = [
            Fleet(),
            Fleet(),
            Fleet()
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

    def get_allotropes(self):
        return self.allotropes

    def get_ships(self):
        return self.ships

    def set_allotropes(self, allotropes):
        self.data_invariant()

        self.allotropes = allotropes

        self.data_invariant()

    def add_ships(self, ships, fleet_index):
        self.data_invariant()

        self.ships = self.ships + ships

        self.get_fleet(fleet_index).append_ships(ships)

        self.data_invariant()

    def get_travel_time(self):
        return mission.DEFAULT_TRAVEL_TIME

    def get_ship_total(self):
        total = 0
        for ship in self.ships:
            total = total + ship.get_points()

        return total

    def get_allotropes_per_tick(self):
        pass

    def tick(self):
        self.data_invariant()

        #print "Tick on %s" % self.get_display_name()
        for fleet in self.get_fleets():
            mission = fleet.get_mission()
            if(mission):
                if(mission.get_stage() == "completed"):
                    fleet.set_mission(None)

            fleet.tick()

        self.data_invariant()

    def data_invariant(self):

        # name
        if not type(self.name) == type(""):
            raise ValueError("Player name must be a str " % str(self.name))
        elif(self.name == ""):
            raise ValueError("Player name must be more than 0 characters: %s", str(self.name))

        # allotropes
        if not type(self.allotropes) == type(1):
            raise ValueError("Player allotropes must be an int  %s" % str(self.allotropes))
        elif(self.allotropes < 0):
            raise ValueError("Player allotropes must be 0 or a posititive int  %s" % str(self.allotropes))

        if not type(self.ships) == type([]):
            raise ValueError("Player ships must be a list  %s" % str(self.ships))

        # workforce
        if not type(self.workforce) == type(1):
            raise ValueError("Player workforce must be an int  %s" % str(self.workforce))
        elif(self.workforce < 0):
            raise ValueError("Player workforce must be 0 or a posititive int  %s" % str(self.workforce))

        # planetary
        if (type(self.planetary) == type(Planetary) or type(self.planetary) == type(None)):
            pass
        else:
            raise ValueError("Player planetary must be None or a Planetary %s" % str(self.planetary))

        # fleets
        if not type(self.fleets[0]) == type(Fleet()):
            raise ValueError("Player fleet must be a Fleet, %s" % str(self.fleets))


class Planetary(GameObject):
    def __init__(self, name=None, owner=None, star_class=0,
                planetary_bodies=None, shields=0,
                defense_system=None, active=True):

        if not name:
            raise PlanetaryException("Needs name")

        self.name = name
        self.owner = owner
        self.star_class = star_class
        self.planetary_bodies = planetary_bodies
        self.shields = shields
        self.defense_system = defense_system

        self.display_name = "%s, a planetary system class %d" \
            % (self.name, self.star_class)

    def get_owner(self):
        return self.owner

    def set_owner(self, owner=None):
        self.owner = owner


class Ship(GameObject):
    def __init__(self, name=None, ship_class=1,
            shields=0, evade=0, hull=100,
            counter_measures=None, guns=0,
            price=0):

        self.name = name
        self.ship_class = ship_class
        self.shields = shields
        self.evade = evade
        self.hull = hull
        self.counter_measures = counter_measures
        self.guns = guns
        self.price = price

        if ship_class == 0:
            raise ShipException("ship_class cannot be %s" % str(ship_class))

        if not price:
            raise ShipException("price cannot be %s" % str(price))

        self.display_name = "%s, a ship, class %d, costing %d" \
            % (self.name, self.ship_class, self.price)

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

    def get_counter_measures(self):
        return self.counter_measures

    def set_hull(self, hull):
        self.hull = hull

    def get_hull(self):
        return self.hull

    def get_guns(self):
        """Return amount of guns."""
        return self.guns

    def get_class_index(self):
        return self.ship_class

    def get_class_name(self):
        return [
            None,
            'Fighter',
            'Cruiser',
            'Destroyer',
            'Dreadnaught',
            'Galactic Supernaught'
        ][self.ship_class]


class Fleet():
    def __init__(self):

        self.ships = []
        self.mission = None

    def assign_ships(self, ships):
        if(type(ships) != type([])):
            raise ValueError("Ships need to come as list, not %s" % str(ships))

        self.ships = ships

    def append_ships(self, ships):
        if(type(ships) != type([])):
            raise ValueError("Ships need to come as list, not %s" % str(ships))

        self.ships = self.ships + ships

    def set_mission(self, mission):
        self.mission = mission

    def get_mission(self):
        return self.mission

    def get_ships(self):
        return self.ships

    def tick(self):
        if(self.mission):
            self.mission.tick()


class GameException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PlanetaryException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PlayersException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ShipException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
