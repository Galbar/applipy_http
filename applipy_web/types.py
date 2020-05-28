import typing as T

from aiohttp import web
from aiohttp_cors import ResourceOptions

CorsConfig = T.Dict[str, ResourceOptions]
ViewMethod = T.Callable[[web.Request], T.Awaitable[web.StreamResponse]]


