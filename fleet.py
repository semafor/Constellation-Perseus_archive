class Fleet():
    def __init__(self):

        self.ships = []
        self.mission = None

        self.data_invariant()

    def assign_ships(self, ships):
        self.data_invariant()

        if(type(ships) != type([])):
            raise ValueError("Ships need to come as list, not %s" % str(ships))

        self.ships = ships

        self.data_invariant()

    def append_ships(self, ships):
        self.data_invariant()

        if(type(ships) != type([])):
            raise ValueError("Ships need to come as list, not %s" % str(ships))

        self.ships = self.ships + ships

        self.data_invariant()

    def remove_ship(self, ship):
        self.data_invariant()

        self.ships.remove(ship)

        self.data_invariant()

    def set_mission(self, mission):
        self.data_invariant()

        self.mission = mission

        self.data_invariant()

    def get_mission(self):
        return self.mission

    def get_ships(self):
        return self.ships

    def tick(self):
        self.data_invariant()

        if(self.mission):
            self.mission.tick()

        self.data_invariant()

    def data_invariant(self):
        if(type(self.ships) != type([])):
            raise ValueError("Ships not a list %s" % str(self.ships))

        if(self.get_mission()):
            mission = self.get_mission()
            try:
                mission.get_stage()
            except:
                raise FleetException("Bad fleet mission %s"\
                    % str(mission.get_stage()))


class FleetException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
