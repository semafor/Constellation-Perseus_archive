import os
import cmd
import game
import shlex

import player
import planetary
import ship


## console.py
## Author:   James Thiele
## Date:     27 April 2004
## Version:  1.0
## Location: http://www.eskimo.com/~jet/python/examples/cmd/
## Copyright (c) 2004, James Thiele
class Console(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "game> "
        self.intro = "Welcome to an Untitled MMO FTL-like text-based spacegame"

    def normalize_query(self, query):
        result = None

        try:
            by_name = self.game.get_by_name(query)
        except:
            by_name = None

        try:
            by_id = self.game.get_by_id(query)
        except:
            by_id = None

        if(by_name):
            result = by_name
        elif(by_id):
            result = [by_id]

        return result

    def do_new(self, args):
        """Create a game object"""
        args = shlex.split(args)

        try:
            what = args[0]
        except:
            print "usage: new type name"
            return

        try:
            name = args[1]
        except:
            print "usage: new type name"
            return

        def _create(x):
            return {
                'player': self.game.create_player,
                'planetary': self.game.create_planetary
            }[x]

        try:
            if(what == "player"):
                args = {
                    "name": name,
                    "allotropes": 1000
                }
            else:
                args = {
                    "name": name
                }

            created = _create(what)(**args)
        except (KeyError):
            print "Error: cannot create something of type %s" % str(what)
            return

        if not created:
            print "Error: player was not created"
            return

        print "Created new %s \"%s\" (%s)" % (what, name, created.get_id())

    def do_get(self, args):
        """Get a game object"""
        if(args == ""):
            print "usage: get id|name"
            return

        res = self.normalize_query(args)

        if(res):
            print "Found %d objects:" % len(res)
            for r in res:
                print "\"%s\" (%s)" % (r.get_display_name(), r.get_id())
            return
        else:
            print "Error: cannot find %s" % str(args)
            return

    def do_st(self, args):
        """Print game status"""
        total = {
            "players": 0,
            "planetaries": 0,
            "ships": 0
        }

        current_tick = self.game.get_current_tick()

        for thing in self.game.get_all_gameobjects():
            if(isinstance(thing, player.Player)):
                total["players"] = total["players"] + 1
            elif(isinstance(thing, planetary.Planetary)):
                total["planetaries"] = total["planetaries"] + 1
            elif(isinstance(thing, ship.Ship)):
                total["ships"] = total["ships"] + 1
            else:
                print "wtf"

        #print "I have registered %d active game things in the universe." % length
        print "Players: %d" % total["players"]
        print "Planetaries: %d" % total["planetaries"]
        print "Ships: %d" % total["ships"]
        print "Current tick: %d" % current_tick

    def do_player_status(self, player_search):
        """Print player status"""
        usage = "usage: player_status id|name"

        if(player_search == ""):
            print usage
            return

        players = self.normalize_query(player_search)

        if not players:
            print "Error: cannot find player %s" % player_search
            return

        print "Found %d players:" % len(players)

        for player in players:
            print player

    def do_player(self, args):
        args = shlex.split(args)
        usage = "usage: <player_id|player_name> <status(st)|attack|abort|buy|systems>"
        usage_player = "usage: <status(st)|attack|abort|buy|systems>"

        usage_attack = "usage attack: <player_id|player_name> <fleet_index>"
        usage_attack_fleet_index = "usage attack player: <fleet_index>"

        usage_defend = "usage defend: <player_id|player_name> <fleet_index>"
        usage_defend_fleet_index = "usage defend player: <fleet_index>"

        usage_abort = "usage abort: <fleet_index>"

        usage_buy = "usage buy: <amount> <ship_enum(ain|beid) [fleet_index]"
        usage_allotropes = "usage add|remove: <amount>"

        usage_system = "usage system: <status(st)|activate|deactivate|install|uninstall> <identifier(wormholeradar)>"

        def _new_mission(self, args, mode):

            if not mode:
                raise ValueError("_new_mission missing mode")

            if(mode == "attack"):
                _usage = usage_attack
                _usage_fleet = usage_attack_fleet_index
            elif(mode == "defend"):
                _usage = usage_defend
                _usage_fleet = usage_defend_fleet_index

            try:
                args[2]
            except:
                print "Error: missing target"
                print _usage
                return

            try:
                args[3]
            except:
                print "Error: missing fleet_index"
                print _usage_fleet
                return

            # target
            try:
                target = self.normalize_query(args[2])[0]
            except:
                print "Error: cannot find player %s" % str(args[2])
                return

            if(player == target):
                print "Error: cannot %s self" % mode
                return

            # fleet
            try:
                fleet_index = int(args[3])
            except:
                print "Error: could not convert fleet index %s to int " % str(args[3])
                return

            try:
                if(mode == "attack"):
                    mission = self.game.attack(player, target, fleet_index, 3)
                elif(mode == "defend"):
                    mission = self.game.defend(player, target, fleet_index, 3)

            except Exception as e:
                print "Failed to attack: %s" % e
                print _usage
                return

            if(mission):
                print "Player %s is %sing player %s. Current stage: %s"\
                    % (mission.get_player().get_name(), mode, mission.get_target().get_name(), mission.get_stage())
                return

        if not args:
            print usage
            return

        """
        Try looking up player
        """
        try:
            player = self.normalize_query(args[0])[0]
        except:
            print "Error: cannot find player %s" % str(args[0])
            return

        """
        Check if there are any actions
        """
        try:
            action = args[1]
        except:
            print usage_player
            return

        """
        Abort
        """
        if(action == "abort"):
            try:
                args[2]
            except:
                print "Error: missing fleet_index"
                print usage_abort
                return

            player.get_fleet(int(args[2])).abort_mission()

        """
        Status
        """
        if(action == "status" or action == "st"):
            self.do_player_status(player.get_id())
            return

        """
        Add/remove (allotropes)
        """
        if(action == "add" or action == "remove"):
            try:
                args[2]
            except:
                print "Error: missing how many allotropes to add/remove"
                print usage_allotropes
                return

            if(action == "add"):
                player.add_allotropes(int(args[2]))
            elif(action == "remove"):
                player.remove_allotropes(int(args[2]))

        """
        Systems
        """
        if(action == "systems"):
            try:
                args[2]
            except:
                print "Error: missing command"
                print usage_system
                return

            try:
                args[3]
            except:
                print "Error: missing system identifier"
                print usage_system
                return

            system_command = args[2]
            system_identifier = args[3]

            if(system_command == "install"):
                system = None

                try:
                    system = self.game.create_planetary_system(system_identifier, player)
                except Exception as e:
                    print "Cannot create %s due to unmet criterion %s" % (system_identifier, e)
                    system = None

                if not system:
                    print "Failed to create system %s" % system_identifier
                    return
                else:
                    print "Created system %s" % system_identifier

                player.get_planetary().install_system(system)
                system.activate()
                return
            else:
                try:
                    system = player.get_planetary().get_system(system_identifier)
                except:
                    print "Planetary lacks system %s" % system_identifier
                    return

            if(system_command == "status" or system_command == "st"):
                print system
                return

            elif(system_command == "activate"):
                system.activate()
                print "System activated"
                print system
                return

            elif(system_command == "deactivate"):
                system.deactivate()
                print "System deactivated"
                print system
                return

            elif(system_command == "upgrade"):
                system.upgrade()
                print "System upgraded"
                print system
                return

            elif(system_command == "downgrade"):
                system.deactivate()
                print "System downgraded"
                print system
                return

            elif(system_command == "uninstall"):
                player.get_planetary().uninstall_system(system)
                print "System uninstalled"
                return

            else:
                print usage_system
                return

        """
        Attack
        """
        if(action == "attack"):
            _new_mission(self, args, action)
            return

        """
        Defend
        """
        if(action == "defend"):
            _new_mission(self, args, action)
            return

        """
        Buy
        """
        if(action == "buy"):

            # amount
            try:
                amount = int(args[2])
            except:
                print usage_buy
                return

            # ship
            try:
                ship_enum = args[3]
            except:
                print usage_buy
                return

            # fleet_index
            try:
                fleet_index = int(args[4])
            except:
                fleet_index = 0

            try:
                result = self.game.buy_ships(player, ship_enum, amount, fleet_index)
            except game.GameException as e:
                print "Failed to buy: %s" % e
                return
            except Exception as e:
                print e
                print usage_buy
                return

            if(result):
                print "Bought %d ships of type %s for player %s (%s)" % (amount, ship_enum, player.get_name(), player.get_id())
            else:
                print "Failed to buy ships."

    def do_status(self, args):
        """See st"""
        self.do_st(args)

    def do_tick(self, args):
        """Control the ticker"""
        if(args == "next"):
            self.game.next_tick()
            print "Current tick: %d" % self.game.get_current_tick()
        else:
            print " \nCurrent tick: %d" % self.game.get_current_tick()
            print "usage: next"

    def do_buy(self, args):
        """Buy ships for a player"""
        args = shlex.split(args)
        help_usage = "usage: buy <player_id|player_name> <ship_enum(ain|beid)> <amount>"

        try:
            player_search = args[0]
        except:
            print help_usage
            return

        player = self.normalize_query(player_search)

        if not player:
            print "Error: cannot find player"
            return
        else:
            player = player[0]

        try:
            ship_enum = args[1]
        except:
            print help_usage
            return

        try:
            amount = int(args[2])
        except:
            print help_usage
            return

        #print "do_buy args: player_id %s, ship_enum: %s, amount %s" % (player_id, ship_enum, amount)

        result = self.game.buy_ships(player, ship_enum, amount)

        if(result):
            print "Bought %d ships of type %s for player %s (%s)" % (amount, ship_enum, player.get_name(), player.get_id())
        else:
            print "Failed to buy ships."

    def do_attack(self, args):
        """Execute attack"""
        args = shlex.split(args)
        help_usage = "usage: attack <attacker> <defender> <fleet_index> <n ticks length of attack>"

        attacker = self.normalize_query(args[0])[0]
        defender = self.normalize_query(args[1])[0]
        fleet_index = int(args[2])
        attack_length = int(args[3])

        mission = self.game.attack(attacker, defender, fleet_index, attack_length)

        if mission:
            print "Player %s is attacking player %s. Current stage: %s" % (mission.get_player().get_name(), mission.get_target().get_name(), mission.get_stage())
        else:
            print "Failed to attack"

    def do_test(self, args):
        print "\n=========\nTesting\n=========\n"
        player_a = self.game.create_random_player(allotropes=1000000)
        print "* new player %s (%s)" % (player_a.get_name(), player_a.get_id())

        player_b = self.game.create_random_player(allotropes=100000)
        print "* new player %s (%s)" % (player_b.get_name(), player_b.get_id())

        player_a_name = player_a.get_name()
        player_b_name = player_b.get_name()

        self.do_player("%s buy 100 ain" % player_a_name)
        self.do_player("%s buy 100 beid" % player_a_name)
        self.do_player("%s buy 10 canopus" % player_a_name)
        self.do_player("%s buy 200 ain" % player_b_name)
        self.do_player("%s buy 200 beid" % player_b_name)

        print player_a
        print player_b

        self.do_player("%s attack %s 0" % (player_a_name, player_b_name))
        for i in range(10):
            self.do_tick("next")

        print "\n=========\nEnd of test\n=========\n"
        print player_a
        print player_b

    def do_system_test(self, args):
        print "\n=========\nSystems testing\n=========\n"

        p = self.game.create_random_player()
        print "* new player %s (%s)" % (p.get_name(), p.get_id())

        self.do_player("%s systems install wormholeradar" % p.get_name())

        # not enough allotropes
        self.do_player("%s add 100" % p.get_name())
        print "* added some allotropes"

        self.do_player("%s systems install wormholeradar" % p.get_name())

        self.do_player("%s systems status wormholeradar" % p.get_name())

        self.do_player("%s systems uninstall wormholeradar" % p.get_name())

        self.do_player("%s systems status wormholeradar" % p.get_name())

        self.do_player("%s systems install wormholeradar" % p.get_name())

        self.do_player("%s systems status wormholeradar" % p.get_name())

        print "\n=========\nEnd of systems testing\n=========\n"

    def do_smalltest(self, args):
        player_a = self.game.create_player(name="a", allotropes=1000000)
        print "* new player %s (%s)" % (player_a.get_name(), player_a.get_id())

        self.do_player("a buy 1 ain")
        self.do_player("a buy 1 beid")
        self.do_player("a buy 1 canopus")

        print player_a

    ## The end of game commands
    #
    #
    #
    #
    #
    ## Command definitions ##
    def do_hist(self, args):
        """Print a list of commands that have been entered"""
        print self._hist

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    ## Command definitions to support Cmd object functionality ##
    def do_EOF(self, args):
        """Exit on system end of file character"""
        return self.do_exit(args)

    def do_shell(self, args):
        """Pass command to a system shell when line begins with '!'"""
        os.system(args)

    def do_help(self, args):
        """Get help on commands
           'help' or '?' with no arguments prints a list of commands
           for which help is available
           'help <command>' or '? <command>' gives help on <command>
        """
        cmd.Cmd.do_help(self, args)

    ## Override methods in Cmd object ##
    def preloop(self):
        """Initialization before prompting user for commands.
           Despite the claims in the Cmd docs, Cmd.preloop() is not a stub.
        """
        cmd.Cmd.preloop(self)   # sets up command completion
        self._hist = []      # No history yet
        self._locals = {}      # Initialize execution namespace for user
        self._globals = {}

        #
        # game stuffs
        #
        self.game = game.Game()

        #player = self.game.create_player(name="Dummy Player", allotropes=10000)
        #print "* new player %s (%s)" % (player.get_name(), player.get_id())

        #planetary = self.game.create(game.Planetary, name="Dummy Planetary")
        #print "* new planetary %s (%s)" % (planetary.get_name(), planetary.get_id())

        #owned_planetary = self.game.create(game.Planetary, name="Owned Planetary")
        #self.game.get_by_id(owned_planetary).set_owner(player)
        #owned_planetary_name = self.game.get_by_id(owned_planetary).get_name()
        #planetary_owner = self.game.get_by_id(self.game.get_by_id(owned_planetary).get_owner()).get_display_name()
        #print "* new planetary %s, (%s) owned by %s" \
        #    % (owned_planetary_name, owned_planetary, planetary_owner)

        #self.game.buy_ships(player, "ain", 4)

    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd docs, Cmd.postloop() is not a stub.
        """
        cmd.Cmd.postloop(self)   # Clean up command completion
        print "Exiting..."

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modifdy the input line
            before execution (for example, variable substitution) do it here.
        """
        self._hist += [line.strip()]
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console,
        return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """
        return stop

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def default(self, line):
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        try:
            exec(line) in self._locals, self._globals
        except Exception, e:
            print e.__class__, ":", e



if __name__ == '__main__':
        console = Console()
        console . cmdloop()
