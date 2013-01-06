import unittest
import ship
import random


class TestShipGunAPI(unittest.TestCase):

    def setUp(self):
        random.seed(0)

        self.ain = ship.Ship(**ship.TYPES["ain"])

    def test_create_ain(self):
        self.assertIsInstance(self.ain, ship.Ship,\
            "Created ain, the Ship")

    def test_gun_states_are_nil(self):
        self.assertEqual(self.ain.get_warm_guns(), 0,\
            "Ship has 0 warm guns")

    def test_gun_with_state_nil_are_lt_nil(self):
        self.assertTrue(self.ain.get_guns_with_temperature(0) > 0,\
            "Ship has more than 0 abs. cold guns")

    def test_ship_attack_tick_warm_guns(self):
        self.ain.attack_tick()

        self.assertTrue(self.ain.get_guns_with_temperature(1) > 0, \
            "Ship has more than 0 guns with state 1")

        self.assertEqual(self.ain.get_guns_with_temperature(0), 0, \
            "There are no absolutely cold guns")

    def test_set_a_guns_temperature(self):
        # fake gun temps
        # nb: needs to be max ains total number of guns
        self.ain.temp_to_guns = {
            0: 0,
            1: 5
        }
        self.ain.set_gun_temperature(1, 0)

        self.assertEqual(self.ain.get_guns_with_temperature(1), 4,\
            "Guns with temp 1 are now 4, down 1")

        self.ain.set_gun_temperature(0, 1)

        self.assertEqual(self.ain.get_guns_with_temperature(0), 0,\
            "Guns with temp 0 are now 0")

    def test_set_multiple_gun_temperatures(self):
        self.ain.set_multiple_gun_temperatures(0, 1, 5)

        self.assertEqual(self.ain.get_guns_with_temperature(0), 0,\
            "Guns with temp 0 are now 0")

        self.assertEqual(self.ain.get_guns_with_temperature(1), 5,\
            "Guns with temp 1 are now 5")

    def test_set_random_gun_temperature(self):

        self.ain.temp_to_guns = {
            0: 1,
            1: 1,
            2: 3
        }

        self.ain.set_random_gun_temperature(-100)

        # random seed 0 returns gun with temp 2
        self.assertEqual(self.ain.get_guns_with_temperature(2), 2,\
            "Randomly selected gun with temp 2 now different temperature")

if __name__ == '__main__':
    unittest.main()
