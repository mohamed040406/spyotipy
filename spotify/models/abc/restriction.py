from typing import Literal


class Restriction:
    __slots__ = ("reason",)

    def __init__(self, data):
        self._update(data)

    def _update(self, data):
        self.reason: Literal["market", "product", "explicit"] = data.pop("reason")
