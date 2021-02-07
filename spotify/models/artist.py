from spotify.models.followers import Followers
from typing import Dict, List, Any

from spotify.models import Image
from spotify.models.abc import BaseArtist


class Artist(BaseArtist):
    def _update(self, data: Dict[str, Any]):
        super(Artist, self)._update(data)
        self.followers = Followers(self.client, data.pop("followers"))
        self.genres: List[str] = data.pop("genres", [])
        self.images: List[Image] = [Image(i) for i in data.pop("images", [])]
        self.popularity: int = int(data.pop("popularity"))
        self.type: str = data.pop("type", "artist")
