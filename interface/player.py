

def status(game, player_search):
    """Print player status"""
    usage = "usage: player_status id|name"

    if(player_search == ""):
        print usage
        return

    players = game.search(player_search)

    if not players:
        print "Error: cannot find player %s" % player_search
        return

    print "Found %d players:" % len(players)

    for player in players:
        print player


def system(game, player, command, identifier):

    usage_system = "usage system:\
        <status(st)|activate|deactivate|install|uninstall>\
        <identifier(wormholeradar)>"

    try:
        command
    except:
        print "Error: missing command"
        print usage_system
        return

    try:
        identifier
    except:
        print "Error: missing system identifier"
        print usage_system
        return

    system_command = command
    system_identifier = identifier

    if(system_command == "install"):

        system = game.install_planetary_system(system_identifier, player)

        if not system:
            print "Failed to create system %s" % system_identifier
            return
        else:
            print "Created system %s" % system_identifier

        player.get_planetary().get_system(system_identifier).activate()

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
        game.uninstall_planetary_system(system, player)
        print "System uninstalled"
        return

    else:
        print usage_system
        return


def _new_mission(game, player, args, mode):

    usage_attack = "usage attack: <player_id|player_name> <fleet_index>"
    usage_attack_fleet_index = "usage attack player: <fleet_index>"

    usage_defend = "usage defend: <player_id|player_name> <fleet_index>"
    usage_defend_fleet_index = "usage defend player: <fleet_index>"

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
        target = game.search(args[2])[0]
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
            mission = game.attack(player, target, fleet_index, 3)
        elif(mode == "defend"):
            mission = game.defend(player, target, fleet_index, 3)

    except Exception as e:
        print "Failed to attack: %s" % e
        print _usage
        return

    if(mission):
        print "Player %s is %sing player %s. Current stage: %s"\
            % (mission.get_player().get_name(),\
                mode, mission.get_target().get_name(), mission.get_stage())
        return

    return mission


def buy(game, player, args):

    usage_buy = "usage buy: <amount> <ship_enum(ain|beid) [fleet_index]"
    available_ships = game.get_available_ships()

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

    if not player.test_criteria(available_ships[ship_enum]["criteria"]):
        print "Player does not meet criteria: %s" %\
            str(available_ships[ship_enum]["criteria"])
        return

    if not player.is_costs_applicable(available_ships[ship_enum]["costs"], coefficient=amount):
        print "Player cannot affor cost: %s" %\
            str(available_ships[ship_enum]["costs"])
        return

    try:
        result = game.buy_ships(player, ship_enum, amount, fleet_index)
    except Exception as e:
        print e
        print usage_buy
        return

    if(result):
        print "Bought %d ships of type %s for player %s (%s)"\
            % (amount, ship_enum, player.get_name(), player.get_id())
    else:
        print "Failed to buy ships."
