import logging
from asyncio import get_event_loop, Future
from typing import Any, List
from collections.abc import Awaitable

import aiohttp_cors
from aiohttp import web
from aiohttp.typedefs import Handler
from applipy import AppHandle
from applipy_http.api import Api
from applipy_http.config import ServerConfig
from applipy_http.types import EndpointHandler


def _adapt_handler(func: EndpointHandler, config: ServerConfig) -> Handler:
    base_ctx = {'server.name': config.name,
                'server.host': config.host,
                'server.port': config.port}

    def wrapper(request: web.Request) -> Awaitable[web.StreamResponse]:
        return func(request, base_ctx.copy())

    return wrapper


class HttpServer(AppHandle):

    def __init__(self, app_runner: web.AppRunner,
                 apis: List[Api],
                 config: ServerConfig,
                 logger: logging.Logger):
        self.runner = app_runner
        self.apis = apis
        self.config = config
        self.logger = logger.getChild(f'http.{config.name}')
        self.future: Future[Any] | None = None

    async def on_init(self) -> None:
        cors = aiohttp_cors.setup(self.runner.app)

        for api in self.apis:
            for route_def in api.get_routes():
                handler = route_def.handler

                route = self.runner.app.router.add_route(
                    route_def.method,
                    route_def.path,
                    _adapt_handler(handler, self.config)
                )

                if route_def.cors_config:
                    cors.add(route, route_def.cors_config)

    async def on_start(self) -> None:
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.config.host, self.config.port)
        await site.start()
        self.logger.info(
            'HTTP server started at http://%s:%s',
            self.config.host,
            self.config.port
        )

        self.future = get_event_loop().create_future()
        await self.future

        self.logger.info('Shutting down HTTP server')
        await self.runner.cleanup()

    async def on_shutdown(self) -> None:
        if self.future is not None:
            self.future.set_result(None)
