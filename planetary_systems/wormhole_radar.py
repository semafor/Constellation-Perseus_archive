from planetary_system import PlanetarySystem


class WormholeRadar(PlanetarySystem):
    """Represents the Wormhole Radar system
        Officially called

            Einstein-Rosen-Podolsky Bridge Signature Antenna (EBSA)

        the antenna picks up any nearby (within n AU) bridges and reports both
        originating and targetted coordinates

    """
    identifier = "wormholeradar"

    def __repr__(self):
        return "Wormhole Radar"

    def __init__(self):
        PlanetarySystem.__init__(self)

    def tick(self, wormholes=[]):

        discovered_wormholes = []

        for hole in wormholes:
            discovered_wormholes.append(hole)

        return discovered_wormholes
