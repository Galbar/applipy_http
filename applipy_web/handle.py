import functools
import logging
from asyncio import sleep
from typing import List, Any

import aiohttp_cors
from aiohttp import web

from applipy import AppHandle, Config
from applipy_web.api.route import Route
from applipy_web.types import ViewMethod, Context
from applipy_metrics.meters.timer import Chronometer
from applipy_metrics.registry import MetricsRegistry

from applipy_web.api.api import Api, ApiName


class WebRequestWrapper:

    def wrap(self, route: Route, func: ViewMethod) -> ViewMethod:
        raise NotImplementedError("Not Implemented")

    def priority(self) -> int:
        """
        The priority defines when the wrapper is applied relative to other
        registered wrappers.
        The highest the priority, the later it is applied (It will wrap all the
        lower priority wrappers)
        """
        return 0


class MetricsRequestWrapper(WebRequestWrapper):

    _metrics: MetricsRegistry
    _metric_name: str
    _priority: int

    def __init__(self, metrics: MetricsRegistry, api_name: ApiName, config: Config) -> None:
        self._metrics = metrics
        metric_infix = '' if not api_name else ('.' + api_name)
        self._metric_name = f'web{metric_infix}.request.time'
        self._priority = config.get(f'web{metric_infix}.metrics.priority', 100)

    def wrap(self, route: Route, func: ViewMethod) -> ViewMethod:
        tags = {
            'method': route.method,
            'path': route.path
        }

        @functools.wraps(func)
        async def wrapper(request: web.Request, context: Context) -> web.StreamResponse:
            chrono = Chronometer()
            try:
                _tags = tags.copy()
                context['metrics.tags'] = _tags
                response = await func(request, context)
                status = response.status
            except web.HTTPException as e:
                status = e.status_code
                raise
            except Exception:
                status = 500
                raise
            finally:
                elapsed = chrono.stop()
                _tags['status'] = status

                self._metrics.timer(self._metric_name, _tags).update(elapsed)

            return response

        return wrapper

    def priority(self) -> int:
        return self._priority


def adapt_handler(func: ViewMethod, ctx: Context) -> Any:
    async def wrapper(request: web.Request) -> web.StreamResponse:
        return await func(request, ctx)

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
                for wrapper in sorted(self.wrappers, key=lambda x: x.priority()):
                    handler = wrapper.wrap(route_def, handler)

                route = self.runner.app.router.add_route(
                    route_def.method,
                    route_def.path,
                    adapt_handler(handler, {})
                )

                if route_def.cors_config:
                    cors.add(route, route_def.cors_config)

    async def on_start(self):
        await self.runner.setup()
        site = web.TCPSite(self.runner, self.host, self.port)
        await site.start()
        self.logger.info(
            'Web application' + (f' `{self.name}` ' if self.name else ' ') + 'started at http://%s:%s',
            self.host,
            self.port
        )
        while True:
            await sleep(3600)

    async def on_shutdown(self):
        self.logger.info('Shutting down web application' + (f' `{self.name}`' if self.name else ''))
        await self.runner.cleanup()
