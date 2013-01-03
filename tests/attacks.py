import unittest
import attack
import fleet
import ship
import force

import player
import planetary


class TestAinVsAin(unittest.TestCase):

    def _build_force(self, ship_type, amount):
        dummy_planetary = planetary.Planetary(name="xy")
        dummy_player = player.Player(name="x", planetary=dummy_planetary)
        flt = fleet.Fleet(owner=dummy_player)
        ships = []
        for i in range(amount):
            ships.append(ship.Ship(**ship.TYPES[ship_type]))

        flt.assign_ships(ships)
        dummy_player.add_ships(ships, 0)
        return force.Force(flt)

    def setUp(self):
        self.one_ain = self._build_force("ain", 1)
        self.one_ain_2 = self._build_force("ain", 1)

        self.one_beid = self._build_force("beid", 1)
        self.one_beid_2 = self._build_force("beid", 1)

        self.two_ain = self._build_force("ain", 2)
        self.two_beid = self._build_force("beid", 2)

    # def test_ain_vs_ain(self):
    #     """Attacking ain dies"""
    #     ain_a = self._build_force("ain", 1)
    #     ain_b = self._build_force("ain", 1)

    #     attack.Attack(ain_a, ain_b)
    #     self.assertEqual(len(ain_a.get_all_ships()), 0)
    #     self.assertEqual(len(ain_b.get_all_ships()), 1)

    # def test_beid_vs_beid(self):
    #     """No beid dies, both live"""
    #     attack.Attack(self.one_beid, self.one_beid_2)
    #     self.assertEqual(len(self.one_beid.get_all_ships()), 1)
    #     self.assertEqual(len(self.one_beid_2.get_all_ships()), 1)

    # def test_beid_vs_ain(self):
    #     """Ain dies, beid lives"""
    #     attack.Attack(self.one_beid, self.one_ain)
    #     self.assertEqual(len(self.one_beid.get_all_ships()), 1)
    #     self.assertEqual(len(self.one_ain.get_all_ships()), 0)

    # def test_two_attacking_ain_vs_single_ain(self):
    #     """The single ain dies, one ain lives"""
    #     attack.Attack(self.two_ain, self.one_ain)

    #     self.assertEqual(len(self.one_ain.get_all_ships()), 0)

    #     attacking_fleet_ships = self.two_ain.get_all_ships()
    #     self.assertEqual(len(attacking_fleet_ships), 1)

    # def test_two_attacking_beid_vs_single_beid(self):
    #     """The single beid dies, two beid lives"""
    #     attack.Attack(self.two_beid, self.one_beid)

    #     self.assertEqual(len(self.one_beid.get_all_ships()), 0)

    #     attacking_fleet_ships = self.two_beid.get_all_ships()
    #     self.assertEqual(len(attacking_fleet_ships), 2)

    def test_ain_vs_ain(self):
        """Something"""

        for scenario in [
            (1, 2), (3, 6), (10, 20), (50, 100), (100, 200), (1000, 2000),
            (2, 1), (6, 3), (20, 10), (100, 50), (200, 100), (2000, 1000),
            (1, 1), (6, 6), (10, 10), (100, 100), (200, 200), (2000, 2000),
            #(100, 100)
            ]:
            _a, _b = scenario
            _a_type, _b_type = ("beid", "ain")
            a = self._build_force(_a_type, _a)
            b = self._build_force(_b_type, _b)

            attack.Attack(a, b)

            #print "\n%d vs %d" % (_a, _b)

            print "Attacker (%d %s)\tlost:\t%d" % (_a, _a_type, _a - len(a.get_all_ships()))
            print "Defender (%d %s)\tlost:\t%d\n" % (_b, _b_type, _b - len(b.get_all_ships()))

    # def test_2000_ain_vs_1000_ain(self):
    #     """Something"""
    #     two_thousand_ain = self._build_force("ain", 2000)
    #     thousand_ain = self._build_force("ain", 1000)

    #     attack.Attack(two_thousand_ain, thousand_ain)

    #     print "\n2000 ain vs 1000 ain:"
    #     print "Originally 2000 ain, there now are %d left" % len(two_thousand_ain.get_all_ships())
    #     print "Originally 1000 ain, there now are %d left" % len(thousand_ain.get_all_ships())

    # def test_1000_ain_vs_2000_ain(self):
    #     """Something"""
    #     two_thousand_ain = self._build_force("ain", 2000)
    #     thousand_ain = self._build_force("ain", 1000)

    #     attack.Attack(thousand_ain, two_thousand_ain)

    #     print "\n1000 ain vs 2000 ain:"
    #     print "Originally 1000 ain, there now are %d left" % len(thousand_ain.get_all_ships())
    #     print "Originally 2000 ain, there now are %d left" % len(two_thousand_ain.get_all_ships())

    # def test_20000_ain_vs_10000_ain(self):
    #     """Something"""
    #     two_thousand_ain = self._build_force("ain", 20000)
    #     thousand_ain = self._build_force("ain", 10000)

    #     attack.Attack([thousand_ain], [two_thousand_ain])

    #     print "\n20000 ain vs 10000 ain:"
    #     print "Originally 10000 ain, there now are %d left" % len(thousand_ain.get_all_ships())
    #     print "Originally 20000 ain, there now are %d left" % len(two_thousand_ain.get_all_ships())

if __name__ == '__main__':
    unittest.main()
