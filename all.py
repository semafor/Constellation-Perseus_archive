import os
import cmd
import game
import shlex


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
            print by_id
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
                    "elements": 1000
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
            if(isinstance(thing, game.Player)):
                total["players"] = total["players"] + 1
            elif(isinstance(thing, game.Planetary)):
                total["planetaries"] = total["planetaries"] + 1
            elif(isinstance(thing, game.Ship)):
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
            print "Status for player \"%s\":" % player.get_name()
            print "\tElements: %d" % player.get_elements()
            print "\tShips: %d (ship points: %d)" % (len(player.get_ships()), player.get_ship_total())

            for n, ship in enumerate(player.get_ships()):
                print "\t\t%i. %s (%s)" % (n + 1, ship.get_name(), ship.get_id())

            print "\tFleets: %d" % (len(player.get_fleets()))

            for n, fleet in enumerate(player.get_fleets()):
                print "\t\tFleet #%i has %s ships." % (n + 1, len(fleet.get_ships()))

                if(fleet.get_mission()):
                    print "\t\t\tOn a mission (%s)" % fleet.get_mission().get_stage()
                else:
                    print "\t\t\tOn base"

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
        player_a = self.game.create(game.Player, name="a", elements=1000)
        print "* new player %s (%s)" % (player_a.get_name(), player_a.get_id())

        self.game.buy_ships(player_a, "ain", 4)
        print "* new player %s %d ships of type %s" % (player_a.get_name(), 4, "ain")

        player_b = self.game.create(game.Player, name="b", elements=1000)
        print "* new player %s (%s)" % (player_b.get_name(), player_b.get_id())

        self.game.buy_ships(player_b, "beid", 3)
        print "* new player %s %d ships of type %s" % (player_b.get_name(), 4, "beid")

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

        player = self.game.create(game.Player, name="Dummy Player", elements=10000)
        print "* new player %s (%s)" % (player.get_name(), player.get_id())

        planetary = self.game.create(game.Planetary, name="Dummy Planetary")
        print "* new planetary %s (%s)" % (planetary.get_name(), planetary.get_id())

        #owned_planetary = self.game.create(game.Planetary, name="Owned Planetary")
        #self.game.get_by_id(owned_planetary).set_owner(player)
        #owned_planetary_name = self.game.get_by_id(owned_planetary).get_name()
        #planetary_owner = self.game.get_by_id(self.game.get_by_id(owned_planetary).get_owner()).get_display_name()
        #print "* new planetary %s, (%s) owned by %s" \
        #    % (owned_planetary_name, owned_planetary, planetary_owner)

        self.game.buy_ships(player, "ain", 4)

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
