
import uuid
from interstellar import mission, ship
from player.player import Player
from planetary.planetary import Planetary
from planetary.name_generator import generate_name
from galaxy.galaxy import Galaxy


class Game:

    """Represents the game

    Exceptions:
        TODO: make sane list of exceptions. current one is a bit insane
    """

    def __init__(self):
        self.game_object_by_uuid = {}
        self.game_object_by_game_object = {}
        self.player_by_name = {}
        self.planetary_by_name = {}
        self.tick = Tick()
        self.galaxy = Galaxy()

        # generate a bunch of rocks in the universe
        self.galaxy.create_random_bodies(1000)

    def search(self, query):
        result = None

        try:
            by_name = self.get_by_name(query)
        except:
            by_name = None

        try:
            by_id = self.get_by_id(query)
        except:
            by_id = None

        if by_name:
            result = by_name
        elif by_id:
            result = [by_id]

        return result

    def create(self, what, **kwargs):
        """Return a GameObject.

        Keyword arguments:
        what -- the GameObject class (default GameObject)
        args -- arguments to pass on to the GameObject class
        """

        if not what:
            raise TypeError('cannot create %s ' % str(what))

        game_object = what(**kwargs)

        # by uid

        game_object_uuid = str(uuid.uuid4())[:5]
        game_object.set_id(game_object_uuid)
        self.game_object_by_uuid[game_object_uuid] = game_object

        # by game_object

        self.game_object_by_game_object[game_object] = game_object_uuid

        return game_object

    def create_random_player(self, **kwargs):
        kwargs['name'] = 'player_%s' % str(uuid.uuid4())[:3]
        return self.create_player(**kwargs)

    def create_player(self, name, **kwargs):
        """Return None if name is empty or already existing username else create a player object and return it."""

        if type('') != type(name):
            name = str(name)
        name = name.strip()
        if len(name) == 0:
            return None
        if name in self.player_by_name:

            # duplicate username

            return None

        kwargs['name'] = name

        # planetary

        try:
            planetary_name = kwargs['planetary_name']
        except:
            planetary_name = None

        if not planetary_name:
            planetary_name = generate_name()

        kwargs['planetary'] = self.create_planetary(name=planetary_name)

        p = self.create(Player, **kwargs)

        kwargs['planetary'].set_owner(p)

        self.player_by_name[name] = p

        return p

    def create_planetary(self, name, **kwargs):
        """Return None if name is empty or already existing username else create a planetary object and return it."""

        if type('') != type(name):
            name = str(name)
        name = name.strip()
        if len(name) == 0:
            return None
        if name in self.planetary_by_name:

            # duplicate planetary name

            return None

        kwargs['name'] = name

        p = self.create(Planetary, **kwargs)

        self.planetary_by_name[name] = p

        self.galaxy.add_body(p)

        return p

    def install_planetary_system(self, identifier, player):
        """Return True if system was installed, False if not"""

        planetary = player.get_planetary()

        system = planetary.get_available_systems()[identifier]()

        if not player.test_criteria(system.criteria):
            return False

        planetary.install_system(system)

        return True

    def uninstall_planetary_system(self, system, player):
        pass
        #player.get_planetary().uninstall_system(system)

    def activate_planetary_system(self, identifier, player):
        system = player.get_planetary().get_system(identifier)

        if not player.is_costs_applicable(system.costs, coefficient=system.get_level()):
            return False

        player.apply_costs(system.costs, coefficient=system.get_level())

        system.activate()

    def deactivate_planetary_system(self, identifier, player):
        system = player.get_planetary().get_system(identifier)

        player.apply_costs(system.costs, revert=True)

        system.deactivate()

    def create_ship(self, **kwargs):
        return self.create(ship.Ship, **kwargs)

    def get_available_ships(self):
        return ship.TYPES

    def buy_ships(
            self,
            buyer,
            ship_enum,
            amount,
            fleet_index=0,
        ):
        """Return False iff not enough allotropes.

        Keyword arguments:
        """

        available_ships = self.get_available_ships()
        ships = []
        costs_args = [available_ships[ship_enum]['costs']]
        costs_kwargs = {"coefficient": amount}

        if not ship_enum:
            raise ShipTypeError('cannot buy ship of %s type'
                                % str(ship_enum))

        if not buyer:
            raise PlayerError('buyer cannot be %s ' % str(buyer))

        if not type(amount) == type(1):
            raise ValueError('amount must be an int: %s' % str(amount))

        if amount < 0:
            raise ValueError('amount must not be negative: %s'
                             % str(amount))

        if buyer.get_fleet(fleet_index).get_mission():
            raise FleetAbsentError('Cannot buy ships for absent fleet')

        try:
            available_ships[ship_enum]
        except:
            return False

        if not buyer.test_criteria(available_ships[ship_enum]['criteria']):
            return False

        if not buyer.is_costs_applicable(*costs_args, **costs_kwargs):
            return False

        buyer.apply_costs(*costs_args, **costs_kwargs)

        for i in range(amount):
            s = self.create_ship(**available_ships[ship_enum])

            ships.append(s)

        buyer.add_ships(ships, fleet_index)

        return True

    def attack(self, *args):
        """Return Mission which will result in an attack

        The Mission will expose its Fleets, as hostile fleets, to the target Planetary when at destination
        """

        return self.create_mission(mission.ATTACK, *args)

    def defend(self, *args):
        """Return Mission which will result in defending a planetary

        The Mission will expose its Fleets, as friendly fleets, to the target Planetary when at destination
        """

        return self.create_mission(mission.DEFEND, *args)

    def create_mission(
        self,
        modus,
        initiator,
        target,
        fleet_index,
        target_stay,
        ):
        """Create and return a Mission"""

        try:
            initiator.get_planetary()
        except:
            raise PlayerError('Initiator invalid: %s' % str(initiator))

        try:
            target.get_planetary()
        except:
            raise PlayerError('Target invalid: %s' % str(target))

        try:
            initiator.get_fleet(fleet_index)
        except:
            raise FleetAbsentError('Fleet %s cannot accept new mission'
                                   % str(fleet_index))

        if type(target_stay) != type(1):
            raise ValueError('Mission stay length invalid: %s'
                             % str(target_stay))

        if len(initiator.get_fleet(fleet_index).get_ships()) == 0:
            raise FleetEmptyError('Fleet %d empty' % fleet_index)
            return False

        if initiator == target:
            raise AttackNotAllowedError('Initiator cannot target self')

        fleet = initiator.get_fleet(fleet_index)

        if fleet.get_mission():
            raise FleetAbsentError('Fleet already on mission')

        m = mission.Mission(modus, initiator, target, target_stay,
                            fleet)
        fleet.set_mission(m)

        # Wormhole in progress, register it

        self.galaxy.register_wormhole(initiator, target)

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
                if name.lower() == obj.get_name().lower():
                    results.append(obj)
            else:

            # case sensitive

                if name == obj.get_name():
                    results.append(obj)

        return results

    def get_all_id(self):
        return self.game_object_by_uuid

    def get_all_gameobjects(self):
        return self.game_object_by_game_object

    def get_all_players(self):
        players = []

        for (name, player) in self.player_by_name.iteritems():
            players.append(player)

        return players

    def get_all_planetaries(self):
        planetaries = []

        for (name, planetary) in self.planetary_by_name.iteritems():
            planetaries.append(planetary)

        return planetaries

    def next_tick(self):
        """Add one to tick and run tick on GameObjects"""

        from time import time

        start = time()
        self.tick.next()

        for p in self.get_all_players():
            p.tick(self)

        for p in self.get_all_planetaries():
            p.tick(self)

        self.galaxy.tick()

        stop = time()
        print round((stop - start) * 1000.0, 2), 'ms'

    def get_current_tick(self):
        """Return current tick"""

        return self.tick.get_tick()


class Tick:

    def __init__(self, genesis=0):
        self.current_tick = genesis

    def next(self):
        """Add one to tick."""

        self.current_tick = self.current_tick + 1

    def get_tick(self):
        """Return current tick."""

        return self.current_tick


class SystemDoesNotExist(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GameError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ShipTypeError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class FleetAbsentError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PlayerError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class FleetEmptyError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class AttackNotAllowedError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
