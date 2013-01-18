from coordinate import Coordinate


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

        coord = Coordinate()
        body._coordinate = coord

        self.coordinates_to_bodies[coord.get_coordinate()] = body
        self.bodies.append(body)

        assert not self._data_invariant()

    def get_body_by_coordinate(self, coordinate):
        return self.coordinates_to_bodies[coordinate]

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

    def tick(self):
        self.purge_wormholes()

    def _data_invariant(self):
        if not __debug__:
            return None
