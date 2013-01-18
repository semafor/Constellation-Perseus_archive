from body import Body
from planetary_systems import wormhole_radar
import attack
import force


class Planetary(Body):
    """Represents a planetary, a star with planetary bodies surrounding it

    Exceptions:
        PlanetaryNameError
            name required, raised if name is empty
        CriterionTypeUnknownError
        CriterionUnmetError
            If system is uninstallable due to unmet criteria
    """
    def __repr__(self):
        return "Planetary System"

    def __init__(self, name=None, owner=None, star_class=0,
                planetary_bodies=None, shields=0,
                defense_system=None, active=True):

        if not name:
            raise PlanetaryNameError("Needs name")

        self.name = name
        self.owner = owner
        self.star_class = star_class
        self.planetary_bodies = planetary_bodies
        self.shields = shields
        self.defense_system = defense_system

        self.systems = {}

        self.hostile_fleets = []
        self.friendly_fleets = []

        self.current_attack = None

        self.display_name = "%s, a planetary system class %d" \
            % (self.name, self.star_class)

    def get_owner(self):
        return self.owner

    def set_owner(self, owner=None):
        self.owner = owner

    def register_hostile_fleet(self, fleet):
        self.hostile_fleets.append(fleet)

    def register_friendly_fleet(self, fleet):
        self.friendly_fleets.append(fleet)

    def get_hostile_fleets(self):
        return self.hostile_fleets

    def get_friendly_fleets(self):
        return self.friendly_fleets

    def install_system(self, system):
        self.systems[system.identifier] = system

    def uninstall_system(self, system):
        self.systems[system.identifier] = None

    def get_system(self, id):
        return self.systems[id]

    def get_installed_systems(self):
        return self.systems

    def can_install_system(self, identifier):
        systems = self.get_available_systems()

        try:
            system = systems[identifier]
        except:
            raise

        try:
            self.is_all_system_criteria_met(system.criteria)
        except:
            raise

        return True

    def get_available_systems(self):
        """Return available systems"""
        return {
            wormhole_radar.WormholeRadar.identifier: wormhole_radar.WormholeRadar
        }

    def is_system_criterion_met(self, criterion):
        """Return True if criterion is met"""
        met = False
        player = self.get_owner()

        if(criterion["type"] == "allotropes"):

            if(player.get_allotropes() >= criterion["value"]):
                met = True
            else:
                raise CriterionUnmetError("Not enough allotropes")

        elif(criterion["type"] == "workforce"):
            if(player.get_workforce() >= criterion["value"]):
                met = True
            else:
                raise CriterionUnmetError("Not enough workforce")

        elif(criterion["type"] == "stellar_class"):
            if(self.star_class >= criterion["value"]):
                met = True
            else:
                raise CriterionUnmetError("Stellar class too low")

        else:
            raise CriterionTypeUnknownError("Unknown criterion type %s" % str(criterion["type"]))

        return met

    def is_all_system_criteria_met(self, criteria):
        met = True
        for criterion in criteria:
            if not self.is_system_criterion_met(criterion):
                met = False

        return met

    def tick(self, wormholes=[]):

        # systems will return stuff
        activity = []
        for k, v in self.systems.iteritems():
            activity.append(v.tick(wormholes))

        if(self.hostile_fleets):

            # register owner fleets if they are not absent
            for fleet in self.get_owner().get_fleets():
                if not fleet.get_mission():
                    self.register_friendly_fleet(fleet)

            self.current_attack = attack.Attack(force.Force(self.hostile_fleets),\
                force.Force(self.friendly_fleets), self)

        self.post_tick_cleanup()

    def post_tick_cleanup(self):
        self.hostile_fleets = []
        self.friendly_fleets = []
        self.current_attack = None


class PlanetaryNameError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CriterionTypeUnknownError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CriterionUnmetError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

