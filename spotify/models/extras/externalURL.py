from typing import Optional


class ExternalURL:
    def __init__(self, data):
        self._update(data)

    def _update(self, data):
        self.spotify: Optional[str] = data.pop("spotify", None)
