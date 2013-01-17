from gameobject import GameObject


class Body(GameObject):
    def __repr__(self):
        return "Body"

    def __str__(self):
        """Return string representation of Body object."""
        if self.owner:
            return "%r: %s, owned by %s at %s"\
                % (self, self.name, self.owner.name, self.get_coordinate())
        else:
            return "%r: %s, without owner at %s"\
                % (self, self.name, self.get_coordinate())

    def get_coordinate(self):
        return self._coordinate
