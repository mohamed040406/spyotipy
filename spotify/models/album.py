from typing import List, Any, Dict

from spotify.models.copyright import Copyright
from spotify.models.abc import BaseAlbum
from spotify.models.simple import SimplifiedTrack
from spotify.models.extras import ExternalID
from spotify.models.abc import Restriction


class Album(BaseAlbum):
    def __iter__(self):
        for track in self.tracks:
            yield track

    async def __aiter__(self):
        for simple in self.tracks:
            yield await simple.get_track()

    def __repr__(self):
        return '<Album id="{0.id}" name="{0.name}">'.format(self)

    def __eq__(self, other):
        return isinstance(other, Album) and other.id == self.id

    def _update(self, data: Dict[str, Any]):
        super(Album, self)._update(data)

        self.copyrights: List[Copyright] = [
            Copyright(i) for i in data.pop("copyrights", [])
        ]
        self.external_ids: ExternalID = ExternalID(data.pop("external_ids"))
        self.genres: List[str] = data.pop("genres", [])
        self.label: str = data.pop("label")
        self.popularity: int = int(data.pop("popularity"))
        self.tracks: List[SimplifiedTrack] = [
            SimplifiedTrack(self.client, i) for i in data.pop("tracks").pop("items")
        ]

        if data.get("restrictions"):
            self.restrictions: Restriction = Restriction(data.pop("restrictions"))
