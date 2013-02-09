from body import Body


class Rock(Body):

    size_thresholds = [
        {
            "low": 0,
            "high": 10,
            "name": "Small Astroid"
        },
        {
            "low": 11,
            "high": 20,
            "name": "Astroid"
        },
        {
            "low": 21,
            "high": 30,
            "name": "Minor Planet"
        },
        {
            "low": 31,
            "high": 40,
            "name": "Planet"
        },
        {
            "low": 41,
            "high": 60,
            "name": "Large Planet"
        },
    ]

    def __repr__(self):
        return self.get_name()

    def __str__(self):
        return "%s size %d" % (self.__repr__(), self.get_size())

    def __init__(self, size=1):

        self.size = size

    def get_size(self):
        return self.size

    def get_name(self):
        size = self.get_size()

        for threshold in self.size_thresholds:
            if(size >= threshold["low"] and size <= threshold["high"]):
                return threshold["name"]
