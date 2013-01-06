import unittest
import attack
import fleet
import ship
import force
import player
import planetary
import random

SHIPS = 100


class TestAinVsAin(unittest.TestCase):

    def _build_force(self, ship_type, amount, playr, attack_mode):
        playr = player.Player(name=playr, planetary=planetary.Planetary(playr))
        flt = fleet.Fleet(owner=playr)
        ships = []
        for i in range(amount):
            ships.append(ship.Ship(**ship.TYPES[ship_type]))

        playr.add_ships(ships, 0)
        flt.assign_ships(ships)

        flt.set_attack_mode(attack_mode)

        return force.Force(flt)

    def _force_diff(self, a, b):
        a_size = len(a.get_all_ships())
        b_size = len(b.get_all_ships())

        a_diff = SHIPS - a_size
        b_diff = SHIPS - b_size

        return "Force A:\t %d (lost %d)\nForce B:\t%d (lost %d)\n" %\
            (a_size, a_diff, b_size, b_diff)

    def setUp(self):
        random.seed(0)
        pass

    def test_ain_vs_ain(self):
        print "\n=======ain,ain"
        a = self._build_force("ain", SHIPS, "player_a", fleet.AGGRESSIVE)
        b = self._build_force("ain", SHIPS, "player_b", fleet.DEFENSIVE)

        attack.Attack(a, b)
        attack.Attack(a, b)
        attack.Attack(a, b)

        print self._force_diff(a, b)

    def test_beid_vs_beid(self):
        print "\n=======beid,beid"

        a = self._build_force("beid", SHIPS, "player_c", fleet.AGGRESSIVE)
        b = self._build_force("beid", SHIPS, "player_d", fleet.DEFENSIVE)

        attack.Attack(a, b)
        attack.Attack(a, b)

        print self._force_diff(a, b)

    def test_beid_vs_ain(self):
        print "\n=======beid,ain"

        a = self._build_force("beid", SHIPS, "player_e", fleet.AGGRESSIVE)
        b = self._build_force("ain", SHIPS, "player_f", fleet.DEFENSIVE)

        attack.Attack(a, b)
        attack.Attack(a, b)
        attack.Attack(a, b)

        print self._force_diff(a, b)

    def test_ain_vs_beid(self):
        print "\n=======ain,beid"

        a = self._build_force("ain", SHIPS, "player_g", fleet.AGGRESSIVE)
        b = self._build_force("beid", SHIPS, "player_h", fleet.DEFENSIVE)

        attack.Attack(a, b)
        attack.Attack(a, b)
        attack.Attack(a, b)
        print self._force_diff(a, b)

if __name__ == '__main__':
    unittest.main()
