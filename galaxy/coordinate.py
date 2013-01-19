from random import randint


class Coordinate():
    def __init__(self):
        self.x = randint(0, 10000)
        self.y = randint(0, 10000)
        self.z = randint(0, 10000)

    def __str__(self):
        return "Coordinate: %s,%s,%s" % (self.x, self.y, self.z)

    def get_coordinate(self):
        return "%s,%s,%s" % (self.get_x(), self.get_y(), self.get_z())

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z
