from galaxy import body
from interstellar import attack, force
import system


class Planetary(body.Body):
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

    def __init__(self, name=None, owner=None, stellar_class=1,
                planetary_bodies=None, shields=0,
                defense_system=None, active=True):

        if not name:
            raise PlanetaryNameError("Needs name")

        self.name = name
        self.owner = owner
        self.stellar_class = stellar_class
        self.planetary_bodies = planetary_bodies
        self.shields = shields

        self.systems = {}

        self.hostile_fleets = []
        self.friendly_fleets = []

        self.current_attack = None

        self.display_name = "%s, a planetary system class %d" \
            % (self.name, self.stellar_class)

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
        del self.systems[system.identifier]

    def get_system(self, id):
        return self.systems[id]

    def get_installed_systems(self):
        return self.systems

    def get_available_systems(self):
        """Return available systems"""
        return {
            system.wormhole_radar.WormholeRadar.identifier: system.wormhole_radar.WormholeRadar
        }

    def tick(self, opened_wormholes=[]):

        # run tick on systems and check that they are still usable
        for k, v in self.systems.iteritems():

            # criteria met?
            self.get_owner().meets_criteria(v.criteria)

            # tick
            v.tick(opened_wormholes)

        # if there's someone on the doorstep, create attack
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
