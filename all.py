import os
import cmd
from game import Game
import shlex
import interface.player
import interface.buy

from player.player import Player
from planetary.planetary import Planetary
from interstellar import ship


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
        self.intro = "Welcome to Constellation Perseus, a MMO FTL-like text-based spacegame"

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

        res = self.game.search(args)

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
            if(isinstance(thing, Player)):
                total["players"] = total["players"] + 1
            elif(isinstance(thing, Planetary)):
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
        interface.player.status(self.game, player_search)

    def do_player(self, args):
        args = shlex.split(args)
        usage = "usage: <player_id|player_name> <status(st)|attack|abort|buy|systems>"
        usage_player = "usage: <status(st)|attack|abort|buy|systems>"

        usage_abort = "usage abort: <fleet_index>"

        usage_allotropes = "usage add|remove: <amount>"

        if not args:
            print usage
            return

        """
        Try looking up player
        """
        try:
            player = self.game.search(args[0])[0]
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
            interface.player.system(self.game, player, args[2], args[3])
            return

        """
        Attack
        """
        if(action == "attack"):
            interface.player._new_mission(self.game, player, args, action)
            return

        """
        Defend
        """
        if(action == "defend"):
            interface.player._new_mission(self.game, player, args, action)
            return

        """
        Buy
        """
        if(action == "buy"):
            interface.player.buy(self.game, player, args)

    def do_status(self, args):
        """See st"""
        self.do_st(args)

    def do_tick(self):
        """Control the ticker"""
        self.game.next_tick()
        print " \nCurrent tick: %d" % self.game.get_current_tick()

    def do_buy(self, args):
        """Buy ships for a player"""
        args = shlex.split(args)
        interface.buy(self.game, args)

    def do_attack(self, args):
        """Execute attack"""
        args = shlex.split(args)
        help_usage = "usage: attack <attacker> <defender> <fleet_index> <n ticks length of attack>"

        attacker = self.game.search(args[0])[0]
        defender = self.game.search(args[1])[0]
        fleet_index = int(args[2])
        attack_length = int(args[3])

        mission = self.game.attack(attacker, defender, fleet_index, attack_length)

        if mission:
            print "Player %s is attacking player %s. Current stage: %s" % (mission.get_player().get_name(), mission.get_target().get_name(), mission.get_stage())
            return
        else:
            print "Failed to attack"
            print help_usage
            return

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
            self.do_tick()

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

        self.do_player("%s st" % p.get_name())

        self.do_player("%s systems install wormholeradar" % p.get_name())

        self.do_player("%s systems status wormholeradar" % p.get_name())

        self.do_player("%s st" % p.get_name())

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

        self.game = Game()

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
