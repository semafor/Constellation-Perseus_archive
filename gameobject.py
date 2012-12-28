class GameObject():
    def get_display_name(self):
        """Return display name."""
        return self.display_name

    def get_name(self):
        """Return name."""
        return self.name

    def set_active(self):
        """Make active True."""
        self.active = True

    def set_inactive(self):
        """Make active False."""
        self.active = False

    def get_active(self):
        """Return active."""
        return self.active

    def get_id(self):
        return self.uuid

    def set_id(self, _uuid):
        self.uuid = _uuid

    def tick(self):
        """Do nothing."""
        pass
