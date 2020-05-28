from typing import Callable

from aiohttp import web

from applipy_web.types import CorsConfig, ViewMethod


class Route:
    method: str
    path: str
    handler: ViewMethod
    cors_config: CorsConfig

    def __init__(self, method: str,
                 path: str,
                 handler: ViewMethod,
                 cors_config: CorsConfig):
        self.method = method
        self.path = path
        self.handler = handler
        self.cors_config = cors_config
