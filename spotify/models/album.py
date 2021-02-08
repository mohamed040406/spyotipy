from typing import List, Any, Dict

from spotify import SpotifyError
from spotify.models.paging import Paging
from spotify.models.copyright import Copyright
from spotify.models.abc import BaseAlbum
from spotify.models.simple import SimplifiedTrack
from spotify.models.extras import ExternalID
from spotify.models.abc import Restriction


class Album(BaseAlbum):
    async def __aiter__(self):
        if self.tracks is None:
            raise SpotifyError("Album Tracks are null???")

        async for simple in self.tracks:
            yield simple

    def __repr__(self):
        return '<Album id="{0.id}" name="{0.name}">'.format(self)

    def __eq__(self, other):
        return isinstance(other, Album) and other.id == self.id

    async def get_all_tracks(self):
        return await self.tracks.get_all_items()

    def _update(self, data: Dict[str, Any]):
        super(Album, self)._update(data)

        self.copyrights: List[Copyright] = [
            Copyright(i) for i in data.pop("copyrights", [])
        ]
        self.external_ids: ExternalID = ExternalID(data.pop("external_ids"))
        self.genres: List[str] = data.pop("genres", [])
        self.label: str = data.pop("label")
        self.popularity: int = int(data.pop("popularity"))

        self.tracks = Paging(self.client, data.pop("tracks"), SimplifiedTrack)

        if data.get("restrictions"):
            self.restrictions: Restriction = Restriction(data.pop("restrictions"))
