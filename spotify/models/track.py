from typing import Dict, Any

from spotify.models.abc import BaseTrack
from spotify.models.extras import ExternalID
from spotify.models.simple import SimplifiedAlbum


class Track(BaseTrack):
    def __init__(self, client, data, *, album=None):
        super(Track, self).__init__(client, data)

        if album:
            self.album = album

    def __repr__(self):
        return '<Track id="{0.id}" name="{0.name}">'.format(self)

    def _update(self, data: Dict[str, Any]):
        super(Track, self)._update(data)
        self.album = SimplifiedAlbum(self.client, data.pop("album"))
        self.popularity: int = int(data.pop("popularity"))
        self.external_ids: ExternalID = ExternalID(data.pop("external_ids"))
