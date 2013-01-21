from system import PlanetarySystem
from criterion import WorkforceCriterion, AllotropeCriterion, StellarClassCriterion


class WormholeRadar(PlanetarySystem):
    """Represents the Wormhole Radar system
        Officially called

            Einstein-Rosen-Podolsky Bridge Signature Antenna (EBSA)

        the antenna picks up any nearby (within n AU) bridges and reports both
        originating and targetted coordinates

    """
    identifier = "wormholeradar"

    # to run/install
    criteria = [
        StellarClassCriterion(0),
        AllotropeCriterion(100, refundable=True),
        WorkforceCriterion(1, refundable=True)
    ]

    def __repr__(self):
        return "Wormhole Radar"

    def __init__(self):
        PlanetarySystem.__init__(self)
        self.discovered_wormholes = []

    def tick(self, wormholes=[]):

        self.discovered_wormholes = []

        for hole in wormholes:
            self.discovered_wormholes .append(hole)

    def get_discovered_wormholes(self):
        return self.discovered_wormholes
