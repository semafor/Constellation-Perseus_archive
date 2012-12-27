DEFAULT_TRAVEL_TIME = 2

ENROUTE = "enroute"
ATTACK = "attack"
DEFENCE = "defence"
COMPETED = "completed"
RETURN = "return"


class Mission():
    def __init__(self, player, target, mission_type, stay_time):

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

        self.player = player
        self.target = target
        self.travel_time = player.get_travel_time()
        self.stay_time = stay_time
        self.mission_type = mission_type

        self.travel_tick = 0

        self.stay_tick = 0

        self.stage = ENROUTE

        self.data_invariant()

    def tick(self):
        self.data_invariant()

        if(self.stage == ENROUTE):
            self.towards_destination()
        elif(self.stage == ATTACK or self.stage == DEFENCE):
            self.at_destination()
        elif(self.stage == RETURN):
            self.towards_base()
        elif(self.stage == COMPETED):
            self.completed()

        self.post_tick_stage_update()

        self.data_invariant()

    def towards_destination(self):
        self.travel_tick = self.travel_tick + 1

    def towards_base(self):
        self.travel_tick = self.travel_tick - 1

    def at_destination(self):
        self.stay_tick = self.stay_tick + 1

    def post_tick_stage_update(self):
        if(self.travel_tick == self.travel_time):
            self.stage = self.mission_type

        if(self.stay_tick == self.stay_time):
            self.stage = RETURN

        if(self.travel_tick == 0):
            self.stage = COMPETED

        if(self.stage == ATTACK):
            self.attack()

        if(self.stage == DEFENCE):
            self.defence()

    def attack(self):
        pass

    def defence(self):
        pass

    def abort(self):
        if(self.travel_tick > 0):
            self.stage = RETURN
        else:
            self.stage = COMPETED

    def completed(self):
        pass

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

    def data_invariant(self):
        # stage
        if not type(self.stage) == type(""):
            raise ValueError("Stage is not a a str: " % str(self.stage))
        elif(self.stage == ""):
            raise ValueError("Stage is an empty string: %s", str(self.stage))
        elif(self.stage != RETURN and self.stage != COMPETED and\
            self.stage != ENROUTE and self.stage != ATTACK\
            and self.stage != DEFENCE):
            raise ValueError("Stage is not %s, but: %s" \
                % (str([ENROUTE, RETURN, COMPETED, ATTACK, DEFENCE]),\
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

        # player, target
        try:
            self.player.get_planetary()
        except:
            raise ValueError("Player is not a Player: %s" % str(self.player))

        try:
            self.target.get_planetary()
        except:
            raise ValueError("Target is not a Player: %s" % str(self.target))


class MissionException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
