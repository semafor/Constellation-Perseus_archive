from planetary_system import PlanetarySystem


class WormholeRadar(PlanetarySystem):
    """Represents the Wormhole Radar system
        Officially called

            Einstein-Rosen-Podolsky Bridge Signature Antenna (EBSA)

        the antenna picks up any nearby (within n AU) bridges and reports both
        originating and targetted coordinates

    """
    identifier = "wormholeradar"

    # to have it running
    criteria = [
        {
            "type": "stellar_class",
            "value": 0
        },
    ]

    # at install
    costs = [
        {
            "type": "allotropes",
            "value": 100
        },
        {
            "type": "free_workforce",
            "value": 1
        }
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
