from typing import Optional

from spotify.models.abc.base import Base


class Object(Base):
    __slots__ = ("id", "client")

    def _update(self, data):
        self.id: Optional[int] = data.pop("id")

    def __repr__(self):
        return self.id

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return issubclass(other, Object) and other.id == self.id
