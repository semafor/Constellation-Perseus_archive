import unittest
import attack
import fleet
import ship


class TestAinVsAin(unittest.TestCase):

    def _build_fleet(self, ship_type, amount):
        flt = fleet.Fleet()
        ships = []
        for i in range(amount):
            ships.append(ship.Ship(**ship.TYPES[ship_type]))

        flt.assign_ships(ships)
        return flt

    def setUp(self):
        self.one_ain = self._build_fleet("ain", 1)
        self.one_ain_2 = self._build_fleet("ain", 1)

        self.one_beid = self._build_fleet("beid", 1)
        self.one_beid_2 = self._build_fleet("beid", 1)

        self.two_ain = self._build_fleet("ain", 2)
        self.two_beid = self._build_fleet("beid", 2)

    def test_ain_vs_ain(self):
        """Attacking ain dies"""
        attack.Attack([self.one_ain], [self.one_ain_2])
        self.assertEqual(len(self.one_ain.get_ships()), 0)
        self.assertEqual(len(self.one_ain_2.get_ships()), 1)

    def test_beid_vs_beid(self):
        """No beid dies, both live"""
        attack.Attack([self.one_beid], [self.one_beid_2])
        self.assertEqual(len(self.one_beid.get_ships()), 1)
        self.assertEqual(len(self.one_beid_2.get_ships()), 1)

    def test_beid_vs_ain(self):
        """Ain dies, beid lives"""
        attack.Attack([self.one_beid], [self.one_ain])
        self.assertEqual(len(self.one_beid.get_ships()), 1)
        self.assertEqual(len(self.one_ain.get_ships()), 0)

    def test_two_attacking_ain_vs_single_ain(self):
        """The single ain dies, two ain lives"""
        attack.Attack([self.two_ain], [self.one_ain])

        self.assertEqual(len(self.one_ain.get_ships()), 0)

        attacking_fleet_ships = self.two_ain.get_ships()
        self.assertEqual(len(attacking_fleet_ships), 2)

    def test_two_attacking_beid_vs_single_beid(self):
        """The single beid dies, two beid lives"""
        attack.Attack([self.two_beid], [self.one_beid])

        self.assertEqual(len(self.one_beid.get_ships()), 0)

        attacking_fleet_ships = self.two_beid.get_ships()
        self.assertEqual(len(attacking_fleet_ships), 2)

    def test_two_hundred_ain_vs_hundred_ain(self):
        """Something"""
        hundred_ain = self._build_fleet("ain", 100)
        two_hundred_ain = self._build_fleet("ain", 200)

        attack.Attack([two_hundred_ain], [hundred_ain])

        print "\nOriginally 200 ain, there now are %d left" % len(two_hundred_ain.get_ships())
        print "Originally 100 ain, there now are %d left" % len(hundred_ain.get_ships())

    def test_2000_ain_vs_1000_ain(self):
        """Something"""
        two_thousand_ain = self._build_fleet("ain", 2000)
        thousand_ain = self._build_fleet("ain", 1000)

        attack.Attack([two_thousand_ain], [thousand_ain])

        print "\nOriginally 2000 ain, there now are %d left" % len(two_thousand_ain.get_ships())
        print "Originally 1000 ain, there now are %d left" % len(thousand_ain.get_ships())

    def test_1000_ain_vs_2000_ain(self):
        """Something"""
        two_thousand_ain = self._build_fleet("ain", 2000)
        thousand_ain = self._build_fleet("ain", 1000)

        attack.Attack([thousand_ain], [two_thousand_ain])

        print "\nOriginally 1000 ain, there now are %d left" % len(thousand_ain.get_ships())
        print "Originally 2000 ain, there now are %d left" % len(two_thousand_ain.get_ships())

if __name__ == '__main__':
    unittest.main()
