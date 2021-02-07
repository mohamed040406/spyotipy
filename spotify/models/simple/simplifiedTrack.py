from typing import Optional

from spotify.models.abc import BaseTrack


class SimplifiedTrack(BaseTrack):
    def __repr__(self):
        return '<SimplifiedTrack id="{0.id}" name="{0.name}">'.format(self)

    async def get_track(self, *, market: Optional[str] = "US"):
        return await self.client.get_track(self.id, market=market)
