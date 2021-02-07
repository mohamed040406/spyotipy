class Base:
    __slots__ = ("client",)

    has_href = True

    def __init__(self, client, data, *args, **kwargs):
        self.client = client
        self._update(data)

    def _update(self, data):
        if self.has_href:
            self.href: str = data.pop("href")
