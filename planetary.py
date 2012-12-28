import gameobject
import attack


class Planetary(gameobject.GameObject):
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

    def tick(self):

        if(self.hostile_fleets):
            # register owner fleets
            for fleet in self.get_owner().get_fleets():
                if not fleet.get_mission():
                    self.register_friendly_fleet(fleet)

            self.current_attack = attack.Attack(self.hostile_fleets,\
                self.friendly_fleets)

        self.post_tick_cleanup()

    def post_tick_cleanup(self):
        self.hostile_fleets = []
        self.friendly_fleets = []
        self.current_attack = None


class PlanetaryException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)