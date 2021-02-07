from typing import Optional


class ExternalID:
    def __init__(self, data):
        self._update(data)

    def _update(self, data):
        self.ean: Optional[str] = data.pop("ean", None)
        self.isrc: Optional[str] = data.pop("isrc", None)
        self.upc: Optional[str] = data.pop("upc", None)
