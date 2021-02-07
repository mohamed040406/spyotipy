from spotify.models.abc.object import Object
from spotify.models.extras.externalURL import ExternalURL


class BaseArtist(Object):
    type = "artist"

    def _update(self, data):
        super(BaseArtist, self)._update(data)

        self.external_urls: ExternalURL = ExternalURL(data["external_urls"])
        self.name: str = data.pop("name")
        self.uri: str = data.pop("uri")
