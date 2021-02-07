from typing import List, Optional, Any, Dict, Literal

from spotify.models.image import Image
from spotify.models.extras import ExternalURL
from spotify.models.abc.restriction import Restriction
from spotify.models.abc.object import Object


class BaseAlbum(Object):
    def __eq__(self, other):
        return isinstance(other, BaseAlbum) and other.id == self.id

    def _update(self, data: Dict[str, Any]):
        from spotify.models.simple.simplifiedArtist import SimplifiedArtist

        super(BaseAlbum, self)._update(data)

        self.album_type: Optional[Literal["album", "single", "compilation"]] = data.pop(
            "album_type", None
        )
        self.artists: List[SimplifiedArtist] = [
            SimplifiedArtist(self.client, i) for i in data.pop("artists")
        ]
        self.available_markets: Optional[List[str]] = (
            data.pop("available_markets") or None
        )

        self.external_urls: ExternalURL = ExternalURL(data.pop("external_urls"))

        self.href: str = data.pop("href")
        self.images: List[Image] = [Image(self.client, i) for i in data.pop("images")]

        self.name: str = data.pop("name")

        self.release_date: str = data.pop("release_date")
        self.release_date_precision: str = data.pop("release_date_precision")

        self.uri: str = data.pop("uri")
        self.type: str = data.pop("type", "album")

        if data.get("restrictions"):
            self.restrictions: Restriction = Restriction(data.pop("restrictions"))
