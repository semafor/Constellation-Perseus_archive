from planetary_system import PlanetarySystem


class StellarShield(PlanetarySystem):
    """Represents the stellar shield system
        When fired upon, it makes planetary susceptible to attacks
        When broken down completely, it destroys the planetary

    """
    identifier = "stellarshield"

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
        return "Stellar Shield"

    def __init__(self):
        PlanetarySystem.__init__(self)

    def tick(self):
        pass
