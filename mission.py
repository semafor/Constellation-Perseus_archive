DEFAULT_TRAVEL_TIME = 3

PREPARATIONS = "preparations"
ENROUTE = "enroute"
RETURN = "return"

ATTACK = "attack"
DEFEND = "defend"

COMPETED = "completed"
ABORTED = "aborted"


class Mission():
    """Represents a mission

    - Takes a fleet out in space and executes a plan
    - Consumes some resources at launch
    - Adds potential gained resources at end

    """
    def __str__(self):

        state = ""

        if(self.get_on_enroute()):
            state = "%sing %s in %d ticks"\
                % (self.get_mission_type(), self.get_target().get_name(), self.get_ticks_until_destination())
        elif(self.get_at_destination()):
            state = "%sing %s, attack tick %d"\
                % (self.get_mission_type(), self.get_target().get_name(), self.get_stay_tick() + 1)
        elif(self.get_on_return()):
            state = "returning in %d ticks"\
                % self.get_ticks_until_base()
        else:
            state = "at base"

        return "\n\tStatus:\t\t%s\
            \n\tDetails:\t%s"\
            % (self.get_stage(), state)

    def __repr__(self):
        return "Mission"

    def __init__(self, mission_type, player, target, stay_time, fleet):

        self.player = player
        self.fleet = fleet
        self.target = target

        self.travel_time = player.get_travel_time()
        self.stay_time = stay_time
        self.mission_type = mission_type

        self.travel_tick = 0

        self.stay_tick = 0

        self.stage = PREPARATIONS

        assert not self._data_invariant()

    def tick(self):
        assert not self._data_invariant()

        if(self.stage == PREPARATIONS):
            self.stage = ENROUTE

        # preparations/enroute
        if(self.get_on_enroute()):
            self.towards_destination()

        # attack/defence
        elif(self.get_at_destination()):
            self.at_destination()

        # return
        elif(self.get_on_return()):
            self.towards_base()

        # completed (unecessary?)
        elif(self.stage == COMPETED):
            self.completed()

        self.post_tick_stage_update()

        assert not self._data_invariant()

    def towards_destination(self):
        assert not self._data_invariant()

        self.travel_tick = self.travel_tick + 1

        assert not self._data_invariant()

    def towards_base(self):
        assert not self._data_invariant()

        self.travel_tick = self.travel_tick - 1

        assert not self._data_invariant()

    def at_destination(self):
        assert not self._data_invariant()

        # register hostile fleet
        if(self.stage == ATTACK):
            self.target.get_planetary().register_hostile_fleet(self.fleet)

        # register friendly fleet
        elif(self.stage == DEFEND):
            self.target.get_planetary().register_friendly_fleet(self.fleet)

        self.stay_tick = self.stay_tick + 1

        # TODO: should be inherited from class (MissionAttack, MissionDefence)
        if(self.mission_type == ATTACK):
            self.attack()
        elif(self.mission_type == DEFEND):
            self.defence()

        assert not self._data_invariant()

    def post_tick_stage_update(self):
        assert not self._data_invariant()

        if(self.travel_tick == self.travel_time):
            self.stage = self.mission_type

        if(self.stay_tick == self.stay_time):
            self.stage = RETURN

        if(self.travel_tick == 0):
            self.completed()

        if(self.stage == ATTACK):
            self.attack()

        if(self.stage == DEFEND):
            self.defence()

        assert not self._data_invariant()

    def attack(self):

        pass

    def defence(self):
        pass

    def abort(self):
        assert not self._data_invariant()

        if(self.travel_tick > 0):
            self.stage = RETURN
        else:
            self.completed()

        assert not self._data_invariant()

    def completed(self):
        assert not self._data_invariant()
        self.fleet.set_mission(None)
        assert not self._data_invariant()

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

    def get_on_enroute(self):
        return (self.stage == ENROUTE)

    def get_on_return(self):
        return (self.stage == RETURN)

    def get_at_destination(self):
        return (self.stage == ATTACK) or (self.stage == DEFEND)

    def get_ticks_until_destination(self):
        if(self.get_on_enroute()):
            return DEFAULT_TRAVEL_TIME - self.get_travel_tick()
        else:
            return None

    def get_ticks_until_base(self):
        if(self.get_on_return()):
            return self.get_travel_tick()
        elif(self.get_at_destination()):
            return self.get_travel_tick() + (self.stay_time - self.get_stay_tick())
        else:
            return None

    def _data_invariant(self):
        if not __debug__:
            return None

        try:
            self.player.get_planetary()
        except:
            raise

        try:
            self.target.get_planetary()
        except:
            raise

        if(self.mission_type != ATTACK) and (self.mission_type != DEFEND):
            raise AssertionError("mission_type invalid: %s"\
                % self.mission_type)

        if not self.stay_time:
            raise AssertionError("Stay time invalid: %s"\
                % str(self.stay_time))

        try:
            self.fleet.get_mission()
        except:
            raise

        # stage
        if not type(self.stage) == type(""):
            raise AssertionError("Stage is not a a str: " % str(self.stage))
        elif(self.stage == ""):
            raise AssertionError("Stage is an empty string: %s", str(self.stage))
        elif(self.stage != RETURN and self.stage != COMPETED and\
            self.stage != ENROUTE and self.stage != ATTACK and\
            self.stage != ABORTED\
            and self.stage != DEFEND and self.stage != PREPARATIONS):
            raise AssertionError("Stage is not %s, but: %s" \
                % (str([PREPARATIONS, ENROUTE, RETURN,\
                    COMPETED, ATTACK, DEFEND]),\
                    str(self.stage)))

        # mission type
        if(self.mission_type != ATTACK and self.mission_type != DEFEND):
            raise AssertionError("Mission type is not %s or %s but: %s"\
                % (ATTACK, DEFEND, str(self.mission_type)))

        # travel tick
        if not type(self.travel_tick) == type(1):
            raise AssertionError("Current tick not a str: %s"\
                % str(self.travel_tick))
        elif(self.travel_tick < 0):
            raise AssertionError("Current tick less than 0: %s"\
                % str(self.travel_tick))
        elif(self.travel_tick > self.travel_time):
            raise AssertionError("Current tick larger than scheduled\
                travel time: %s" % str(self.travel_tick))

        # player, fleet, target
        try:
            self.fleet.get_mission()
        except:
            raise
