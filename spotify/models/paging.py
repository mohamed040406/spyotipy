import re
from typing import Dict, Any, Optional, Callable

from spotify import SpotifyError
from spotify.http import Route
from spotify.models.abc import Base

_PAG_API_REGEX = re.compile(r"https?://api\.spotify\.com/v\d/(.*)/(.+)(?=\?)")


class Paging:
    def __init__(
            self,
            client,
            data: Dict[str, Any],
            _type: Callable[[Any, Dict[str, Any]], Base],
            *,
            limit: int = 50,
            offset: int = 0
    ):
        self.__type__ = _type
        self.client = client
        self._update(data)

        self.limit = limit
        self.offset = offset

    def _update(self, data: Dict[str, Any]):
        self.total: int = int(data.pop("total"))
        self._next: Optional[str] = data.pop("next", None)
        self._previous: Optional[str] = data.get("previous", None)

        match = re.match(_PAG_API_REGEX, data.pop("href", ""))
        if not match:
            raise ValueError("Failed to get the spotify api href")

        self.link = match.group()

        self.current = list(map(lambda i: self.__type__(self.client, i), data.pop("items")))

    async def get_all_items(self):
        return [item async for item in self]

    async def previous(self):
        if self._previous is None:
            raise SpotifyError("There are no pages")

        route = Route("GET", self._previous, prefix=False)
        data = await self.client.http.request(route)

        self._update(data)

    async def next(self):
        if self._next is None:
            raise SpotifyError("There are no other pages")

        route = Route("GET", self._next, prefix=False)
        data = await self.client.http.request(route)

        self._update(data)

    async def __aiter__(self):
        total: Optional[int] = self.total or None
        current = offset = self.offset

        if total is not None and current > total:
            raise SpotifyError("Offset can't be greater than total")

        while total is None or current < total:
            route = Route(
                "GET", self.link + "?offset={offset}&limit={limit}",
                prefix=False, offset=offset, limit=self.limit
            )

            data = await self.client.http.request(route)

            if total is None:
                total = int(data.pop("total", 0))

            items = data.pop("items", [])
            for item in items:
                current += 1
                yield self.__type__(self.client, item)

            offset += self.limit
