DEFAULT_TRAVEL_TIME = 3

PREPARATIONS = "preparations"
ENROUTE = "enroute"
RETURN = "return"

ATTACK = "attack"
DEFENCE = "defence"

COMPETED = "completed"
ABORTED = "aborted"


class Mission():
    def __init__(self, player, target, mission_type, stay_time, fleet):

        try:
            player.get_planetary()
        except:
            raise ValueError("Player needs to be Player, not %s" % str(player))

        try:
            target.get_planetary()
        except:
            raise ValueError("Target needs to be Player, not %s" % str(target))

        if not mission_type == ATTACK or mission_type == DEFENCE:
            raise ValueError("mission_type needs to be %s or %s, not %s"\
                % (ATTACK, DEFENCE, str(mission_type)))

        if not stay_time:
            raise ValueError("need to %s n ticks, not %s"\
                % (mission_type, str(stay_time)))

        try:
            fleet.get_mission()
        except:
            raise ValueError("Bad given fleet: %s"\
                % str(fleet))

        self.player = player
        self.fleet = fleet
        self.target = target

        self.travel_time = player.get_travel_time()
        self.stay_time = stay_time
        self.mission_type = mission_type

        self.travel_tick = 0

        self.stay_tick = 0

        self.stage = PREPARATIONS

        self._data_invariant()

    def tick(self):
        self._data_invariant()

        if(self.stage == PREPARATIONS):
            self.stage = ENROUTE

        # preparations/enroute
        if(self.stage == ENROUTE):
            self.towards_destination()

        # attack/defence
        elif(self.stage == ATTACK or self.stage == DEFENCE):
            self.at_destination()

        # return
        elif(self.stage == RETURN):
            self.towards_base()

        # completed (unecessary?)
        elif(self.stage == COMPETED):
            self.completed()

        self.post_tick_stage_update()

        self._data_invariant()

    def towards_destination(self):
        self._data_invariant()

        self.travel_tick = self.travel_tick + 1

        self._data_invariant()

    def towards_base(self):
        self._data_invariant()

        self.travel_tick = self.travel_tick - 1

        self._data_invariant()

    def at_destination(self):
        self._data_invariant()

        # register hostile fleet
        if(self.stage == ATTACK):
            self.target.get_planetary().register_hostile_fleet(self.fleet)

        # register friendly fleet
        elif(self.stage == DEFENCE):
            self.target.get_planetary().register_friendly_fleet(self.fleet)

        self.stay_tick = self.stay_tick + 1

        if(self.mission_type == ATTACK):
            self.attack()
        elif(self.mission_type == DEFENCE):
            self.defence()
        else:
            raise MissionException("at_destination in unknown state %s"\
                % str(self.mission_type))

        self._data_invariant()

    def post_tick_stage_update(self):
        self._data_invariant()

        if(self.travel_tick == self.travel_time):
            self.stage = self.mission_type

        if(self.stay_tick == self.stay_time):
            self.stage = RETURN

        if(self.travel_tick == 0):
            self.completed()

        if(self.stage == ATTACK):
            self.attack()

        if(self.stage == DEFENCE):
            self.defence()

        self._data_invariant()

    def attack(self):

        pass

    def defence(self):
        pass

    def abort(self):
        self._data_invariant()

        if(self.travel_tick > 0):
            self.stage = RETURN
        else:
            self.completed()

        self._data_invariant()

    def completed(self):
        self._data_invariant()
        self.fleet.set_mission(None)
        self._data_invariant()

    def get_player(self):
        return self.player

    def get_target(self):
        return self.target

    def get_mission_type(self):
        return self.mission_type

    def get_travel_tick(self):
        return self.travel_tick

    def get_stay_tick(self):
        return self.stay_tick

    def get_stage(self):
        return self.stage

    def _data_invariant(self):
        # stage
        if not type(self.stage) == type(""):
            raise ValueError("Stage is not a a str: " % str(self.stage))
        elif(self.stage == ""):
            raise ValueError("Stage is an empty string: %s", str(self.stage))
        elif(self.stage != RETURN and self.stage != COMPETED and\
            self.stage != ENROUTE and self.stage != ATTACK and\
            self.stage != ABORTED\
            and self.stage != DEFENCE and self.stage != PREPARATIONS):
            raise ValueError("Stage is not %s, but: %s" \
                % (str([PREPARATIONS, ENROUTE, RETURN,\
                    COMPETED, ATTACK, DEFENCE]),\
                    str(self.stage)))

        # mission type
        if(self.mission_type != ATTACK and self.mission_type != DEFENCE):
            raise ValueError("Mission type is not %s or %s but: %s"\
                % (ATTACK, DEFENCE, str(self.mission_type)))

        # travel tick
        if not type(self.travel_tick) == type(1):
            raise ValueError("Current tick is not a str: %s"\
                % str(self.travel_tick))
        elif(self.travel_tick < 0):
            raise ValueError("Current tick is less than 0: %s"\
                % str(self.travel_tick))
        elif(self.travel_tick > self.travel_time):
            raise MissionException("Current tick is larger than scheduled\
                travel time: %s" % str(self.travel_tick))

        # player, fleet, target
        try:
            self.player.get_planetary()
        except:
            raise ValueError("Player is not a Player: %s" % str(self.player))

        try:
            self.fleet.get_mission()
        except:
            raise ValueError("Bad fleet: %s" % str(self.flet))

        try:
            self.target.get_planetary()
        except:
            raise ValueError("Target is not a Player: %s" % str(self.target))


class MissionException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
