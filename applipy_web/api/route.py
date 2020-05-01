from typing import Callable

from aiohttp import web

from applipy_web.api.cors import CorsConfig


Handler = Callable[[web.Request], web.StreamResponse]


class Route:
    method: str
    path: str
    handler: Handler
    cors_config: CorsConfig

    def __init__(self, method: str,
                 path: str,
                 handler: Handler,
                 cors_config: CorsConfig):
        self.method = method
        self.path = path
        self.handler = handler
        self.cors_config = cors_config
