from typing import Optional
from spotify.models.abc.base import Base


class Image(Base):
    has_href = False

    def _update(self, data):
        super()._update(data)

        self.url: str = data.pop("url")
        self.height: Optional[int] = data.pop("height", None)
        self.width: Optional[int] = data.pop("width", None)
