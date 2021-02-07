from spotify.models.abc import Base


class Followers(Base):
    def _update(self, data):
        super()._update(data)
        self.total: int = int(data.pop("total"))
