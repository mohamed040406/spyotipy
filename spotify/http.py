import asyncio
import logging
import sys
from base64 import b64encode
from collections import defaultdict
from typing import Optional, Dict
from urllib.parse import quote as _uriquote

import aiohttp as aiohttp

from . import __version__
from .errors import Forbidden, NotFound, ServerError, HTTPException, BearerError

log = logging.getLogger(__name__)


class Route:
    BASE = 'https://api.spotify.com/v1'

    def __init__(self, method, path, **parameters):
        self.path = path
        self.method = method

        url = (self.BASE + self.path)
        if parameters:
            self.url = url.format(**{k: _uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()})
        else:
            self.url = url

    @property
    def bucket(self):
        return "{0.method} {0.path}".format(self)


class Locker:
    def __init__(self, lock):
        self.lock = lock
        self._unlock = True

    def __enter__(self):
        return self

    def unlock(self):
        self._unlock = False

    def __exit__(self, type, value, traceback):
        if self._unlock:
            self.lock.release()


class HTTP:
    """An http Client to handle Requests to Spotify API"""

    SUCCESS_LOG = '{method} {url} has received {text}'
    REQUEST_LOG = '{method} {url} with {json} has returned {status}'

    MAX_TRIES = 5

    def __init__(self, client_id: str, client_secret: str, *, loop=None):
        self.loop = loop if loop else asyncio.get_event_loop()
        self.__session = aiohttp.ClientSession(loop=self.loop)

        self.bearer_info: Optional[Dict[str, str]] = None

        self.client_id = client_id
        self.client_secret = client_secret

        self.__locks = defaultdict(asyncio.Lock)

        self.__global = asyncio.Event()
        self.__global.set()

        self.user_agent = 'https://github.com/mohamed040406/SpotifyPy {0} Python/{1[0]}.{1[1]} aiohttp/{2}'.format(
            __version__, sys.version_info, aiohttp.__version__
        )

    async def request(self, route: Route, **kwargs):
        method = route.method
        url = route.url
        bucket = route.bucket

        headers = kwargs.pop("headers", {})
        if "Authorization" not in headers:
            if self.bearer_info is None:
                self.bearer_info = bearer_info = await self.get_bearer_info()
                access_token = bearer_info["access_token"]
            else:
                access_token = self.bearer_info["access_token"]

            headers["Authorization"] = "Bearer " + access_token

        headers = {
            "User-Agent": self.user_agent,
            "X-Ratelimit-Precision": "millisecond",
            "Content-Type": "application/json",
            **headers
        }

        if bucket is not None:
            lock = self.__locks[route.bucket]
        else:
            lock = asyncio.Lock()

        if not self.__global.is_set():
            await self.__global.wait()

        async with lock:
            for tries in range(self.MAX_TRIES):
                async with self.__session.request(method, url, headers=headers, **kwargs) as res:
                    log.debug('%s %s with %s has returned %s', method, url, kwargs.get('data'), res.status)
                    data = await res.json()
                    if 300 > res.status >= 200:
                        log.debug('%s %s has received %s', method, url, data)
                        return data

                    if res.status == 429:
                        self.__global.clear()

                        fmt = "We are being rate limited. " \
                              "Retrying in %.2f seconds. " \
                              "Bucket: \"%s\""

                        limit = int(res.headers.get("Retry-After"))
                        log.warning(fmt, limit, bucket)

                        async with self.__global:
                            self.__global.clear()
                            await asyncio.sleep(int(limit), loop=self.loop)
                            self.__global.set()

                            log.debug('Done sleeping for the rate limit. Retrying...')

                    if res.status in {500, 502}:
                        await asyncio.sleep(1 + self.MAX_TRIES * 2)
                        continue

                        # the usual error cases
                    if res.status == 403:
                        raise Forbidden(res, data)
                    elif res.status == 404:
                        raise NotFound(res, data)
                    elif res.status == 503:
                        raise ServerError(res, data)
                    else:
                        raise HTTPException(res, data)

    async def close(self):
        """Close the HTTP session."""
        await self.__session.close()

    async def get_bearer_info(self):
        client_id = self.client_id
        client_secret = self.client_secret

        token = b64encode(":".join((client_id, client_secret)).encode())

        data = {"grant_type": "client_credentials"}
        headers = {"Authorization": f"Basic {token.decode()}"}

        session = self.__session

        async with session.post(
                "https://accounts.spotify.com/api/token", data=data, headers=headers
        ) as response:
            bearer_info = await response.json(encoding="utf-8")

            if "error" in bearer_info.keys():
                raise BearerError(response=response, message=bearer_info)

        return bearer_info

    # Endpoint related methods (defined in order)

    # Albums endpoints
    async def get_albums(self, ids, *, market: Optional[str] = "US"):
        route = Route("GET", "/albums", ids=ids, market=market)

        return await self.request(route)

    async def get_album(self, _id: str, *, market: Optional[str] = "US"):
        route = Route("GET", "/albums/%s" % _id, market=market)
        return await self.request(route)

    async def get_album_tracks(
            self,
            _id: str,
            *,
            market: Optional[str] = "US",
            limit: Optional[int] = 20,
            offset: Optional[int] = 0,
    ):
        if limit < 1 or limit > 50:
            raise ValueError("Limit should be an int between 1 and 5")
        route = Route("GET", "/albums/%s/tracks" % _id, market=market, limit=limit, offset=offset)

        return await self.request(route)

    # Tracks endpoints
    async def get_track(self, _id: str, *, market: Optional[str] = "US"):
        route = Route("GET", "/tracks/%s" % _id, market=market)

        return await self.request(route)
