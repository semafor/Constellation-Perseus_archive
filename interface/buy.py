#!/usr/bin/python
# -*- coding: utf-8 -*-


def buy(game, args):
    help_usage = \
        'usage: buy <player_id|player_name> <ship_enum(ain|beid)> <amount>'

    try:
        player_search = args[0]
    except:
        print help_usage
        return

    player = game.search(player_search)

    if not player:
        print 'Error: cannot find player'
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

    result = game.buy_ships(player, ship_enum, amount)

    if result:
        print 'Bought %d ships of type %s for player %s (%s)' \
            % (amount, ship_enum, player.get_name(), player.get_id())
    else:
        print 'Failed to buy ships.'
