from typing import List, Dict, Any, Optional

from spotify.models.abc.object import Object
from spotify.models.extras.externalURL import ExternalURL
from spotify.models.abc.restriction import Restriction


class BaseTrack(Object):
    def _update(self, data: Dict[str, Any]):
        from spotify.models.simple import SimplifiedArtist

        super(BaseTrack, self)._update(data)
        self.artists: List[SimplifiedArtist] = [
            SimplifiedArtist(self.client, i) for i in data.pop("artists", [])
        ]
        self.available_markets: Optional[List[str]] = data.pop("available_markets", None)
        self.disc_number: Optional[int] = int(data.pop("disc_number"))
        self.duration_ms: int = int(data.pop("duration_ms"))
        self.explicit: bool = bool(data.pop("explicit"))
        self.external_urls: ExternalURL = ExternalURL(data.pop("external_urls", None))
        self.href: str = data.pop("href")
        self.is_local: bool = bool(data.pop("is_local", False))

        self.name: str = data.pop("name")
        self.preview_url: Optional[str] = data.pop("preview_url", None)
        self.type: str = data.pop("type", "track")

        self.track_number: int = int(data.pop("track_number"))
        self.uri: str = data.pop("uri")

        self.linked_from: Optional[BaseTrack] = (
            BaseTrack(self.client, data.pop("linked_from"))
            if data.get("linked_from")
            else None
        )

        self.is_playable: Optional[bool] = data.pop("is_playable", None)

        if data.get("restrictions"):
            self.restrictions: Restriction = Restriction(data.pop("restrictions"))
        else:
            self.restrictions = None
