from typing import Any, Dict, Optional

from spotify.models.abc import BaseAlbum


class SimplifiedAlbum(BaseAlbum):
    def __repr__(self):
        return '<SimplifiedAlbum id="{0.id}" name="{0.name}">'.format(self)

    def _update(self, data: Dict[str, Any]):
        super(SimplifiedAlbum, self)._update(data)

        self.album_group: Optional[str] = data.pop("album_group", None)
