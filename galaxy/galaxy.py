from coordinate import Coordinate
from random import randint
from rock import Rock
import math

DISTANCE_UNIT = "parsec"


class Galaxy():
    """Represents the galaxy, the home of Planetaries, Outposts, Rocks (bodies)

    - Holds all bodies
    - Keeps track of Wormholes

    """
    def __init__(self):

        self.coordinates_to_bodies = {}
        self.bodies = []
        self.wormholes = []

        assert not self._data_invariant()

    def add_body(self, body):
        assert not self._data_invariant()

        coord = self.new_coordinate()

        body._coordinate = coord

        self.coordinates_to_bodies[coord.get_coordinate()] = body
        self.bodies.append(body)

        assert not self._data_invariant()

    def new_coordinate(self):

        while(True):
            c = Coordinate()
            if not self.coordinate_exist(c):
                return c

    def get_body_by_coordinate(self, coordinate):
        return self.coordinates_to_bodies[coordinate]

    def coordinate_exist(self, coordinate):
        try:
            self.get_body_by_coordinate(coordinate)
        except:
            return False

        return True

    def get_bodies(self):
        return self.bodies

    def remove_body(self, body):
        assert not self._data_invariant()

        self.bodies.remove(body)
        self.coordinates_to_bodies[body._coordinate.get_coordinate()] = None

        assert not self._data_invariant()

    def register_wormhole(self, origin, target):
        assert not self._data_invariant()

        self.wormholes.append({
            "origin": origin.get_planetary().get_coordinate().get_coordinate(),
            "target": target.get_planetary().get_coordinate().get_coordinate()
        })

        assert not self._data_invariant()

    def get_wormholes(self):
        return self.wormholes

    def purge_wormholes(self):
        assert not self._data_invariant()

        self.wormholes = []

        assert not self._data_invariant()

    def get_neighbouring_bodies(self, body):
        return self.get_nearby_bodies(body.get_coordinate())

    def get_nearby_bodies(self, coordinate, max_distance=170):
        """Return bodies less than n parsecs from coordinate"""

        bodies = []

        for body in self.get_bodies():
            distance = self.get_distance(coordinate, body.get_coordinate())

            if distance == 0:
                continue

            if distance >= max_distance:
                continue

            bodies.append(body)

        return bodies

    def get_distance(self, a, b):
        xa, ya, za = (a.get_x(), a.get_y(), a.get_z())
        xb, yb, zb = (b.get_x(), b.get_y(), b.get_z())

        return math.sqrt((xa - xb) ** 2 + (ya - yb) ** 2 + (za - zb) ** 2)

    def create_random_bodies(self, amount):

        for i in range(amount):
            size = randint(1, 60)
            rock = Rock(size=size)
            self.add_body(rock)

    def tick(self):
        self.purge_wormholes()

    def _data_invariant(self):
        if not __debug__:
            return None
