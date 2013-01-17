from coordinate import Coordinate


class Galaxy():
    """Represents the galaxy, the home of Planetaries, Outposts, Rocks (bodies)

    """
    def __init__(self):

        self.coordinates_to_bodies = {}
        self.bodies = []

    def add_body(self, body):
        coord = Coordinate()
        body._coordinate = coord

        self.coordinates_to_bodies[coord.get_coordinate()] = body
        self.bodies.append(body)

    def get_body_by_coordinate(self, coordinate):
        return self.coordinates_to_bodies[coordinate]

    def get_bodies(self):
        return self.bodies

    def remove_body(self, body):
        self.bodies.remove(body)
        self.coordinates_to_bodies[body._coordinate.get_coordinate()] = None
