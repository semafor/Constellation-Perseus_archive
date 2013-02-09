from system import PlanetarySystem
from criterion import StellarClassCriterion
from costs import WorkforceCost
from random import randint


class GravitationLensDetector(PlanetarySystem):
    """Represents the Gravitational Lens Detector system which
    detects nearby bodies.

    Official name:
        The Gravitational Microlensing Extra-Stellar Body Detector (GRAMEBO)
    """
    identifier = "gramebo"

    # to run/install
    criteria = [
        StellarClassCriterion(0)
    ]
    costs = [
        WorkforceCost(1, refundable=True)
    ]

    def __repr__(self):
        return "Gravitational Lens Detector"

    def __init__(self):
        PlanetarySystem.__init__(self)
        self.discovered_bodies = []

    def tick(self, game, planetary):
        planetary_coords = planetary.get_coordinates()
        all_local_bodies = game.galaxy.get_nearby_bodies(planetary_coords)

        for body in all_local_bodies:
            if randint(0, 100) < 10:
                self.discovered_bodies.append(body)

    def get_discovered_bodies(self):
        return self.discovered_bodies
