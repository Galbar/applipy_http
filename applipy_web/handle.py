import functools
import logging
from asyncio import sleep
from typing import List

import aiohttp_cors
from aiohttp import web

from applipy import AppHandle
from applipy_web.api.route import Route
from applipy_web.types import ViewMethod
from applipy_metrics.meters.timer import Chronometer
from applipy_metrics.registry import MetricsRegistry

from applipy_web.api.api import Api, ApiName


class WebRequestWrapper:

    def wrap(self, route: Route, func: ViewMethod) -> ViewMethod:
        raise NotImplementedError("Not Implemented")


class MetricsRequestWrapper(WebRequestWrapper):

    _metrics: MetricsRegistry
    _metric_name: str

    def __init__(self, metrics: MetricsRegistry, api_name: ApiName) -> None:
        self._metrics = metrics
        metric_infix = '' if not api_name else ('.' + api_name)
        self._metric_name = f'web{metric_infix}.request.time'

    def wrap(self, route: Route, func: ViewMethod) -> ViewMethod:
        tags = {
            'method': route.method,
            'path': route.path
        }
        @functools.wraps(func)
        async def wrapper(request: web.Request) -> web.StreamResponse:
            chrono = Chronometer()
            try:
                response = await func(request)
                status = response.status
            except Exception:
                status = 500
                raise
            finally:
                elapsed = chrono.stop()
                _tags = tags.copy()
                _tags['status'] = status

                self._metrics.timer(self._metric_name, _tags).update(elapsed)

            return response

        return wrapper


class WebConfig:

    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port


class WebHandle(AppHandle):

    def __init__(self, web_app_runner: web.AppRunner,
                 apis: List[Api],
                 config: WebConfig,
                 wrappers: List[WebRequestWrapper],
                 logger: logging.Logger):
        self.runner = web_app_runner
        self.apis = apis
        self.name = config.name
        self.host = config.host
        self.port = config.port
        self.logger = logger
        self.wrappers = wrappers

    async def on_init(self):
        cors = aiohttp_cors.setup(self.runner.app)

        for api in self.apis:
            for route_def in api.get_routes():
                handler = route_def.handler
                for wrapper in self.wrappers:
                    handler = wrapper.wrap(route_def, handler)

                route = self.runner.app.router.add_route(
                    route_def.method,
                    route_def.path,
                    handler
                )

                if route_def.cors_config:
                    cors.add(route, route_def.cors_config)

    async def on_start(self):
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.host, self.port)
        await site.start()
        self.logger.info(
            'Application started at http://%s:%s',
            self.host,
            self.port
        )
        while True:
            await sleep(3600)

    async def on_shutdown(self):
        self.logger.info('Shutting down web application')
        await self.runner.cleanup()
