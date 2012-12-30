import unittest
import attack
import fleet
import ship
import force


class TestAinVsAin(unittest.TestCase):

    def _build_force(self, ship_type, amount):
        flt = fleet.Fleet()
        ships = []
        for i in range(amount):
            ships.append(ship.Ship(**ship.TYPES[ship_type]))

        flt.assign_ships(ships)
        return force.Force(flt)

    def setUp(self):
        pass

    def test_ain_vs_ain(self):
        """Attacking ain dies"""
        ain_a = self._build_force("ain", 1)
        ain_b = self._build_force("ain", 1)

        attack.Attack(ain_a, ain_b)
        self.assertEqual(len(ain_a.get_all_ships()), 0)
        self.assertEqual(len(ain_b.get_all_ships()), 1)

if __name__ == '__main__':
    unittest.main()
