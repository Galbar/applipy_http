import functools
import logging
from asyncio import sleep
from typing import List

import aiohttp_cors
from aiohttp import web

from applipy import AppHandle
from applipy_metrics.meters.timer import Chronometer
from applipy_metrics.registry import MetricsRegistry

from applipy_web.api.api import Api


def _response_status_timer(func, name, registry, tags):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        chrono = Chronometer()
        try:
            response = await func(*args, **kwargs)
            status = response.status
        except Exception:
            status = 500
            raise
        finally:
            elapsed = chrono.stop()
            _tags = tags.copy()
            _tags['status'] = status

            registry.timer(name, _tags).update(elapsed)

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
                 logger: logging.Logger,
                 metrics: MetricsRegistry):
        self.runner = web_app_runner
        self.apis = apis
        self.name = config.name
        self.host = config.host
        self.port = config.port
        self.logger = logger
        self.metrics = metrics

    async def on_init(self):
        cors = aiohttp_cors.setup(self.runner.app)

        metric_infix = '' if self.name is None else '.' + self.name
        metric_name = f'web{metric_infix}.request.time'

        for api in self.apis:
            for route_def in api.get_routes():
                tags = {
                    'method': route_def.method,
                    'path': route_def.path
                }
                route = self.runner.app.router.add_route(
                    route_def.method,
                    route_def.path,
                    _response_status_timer(
                        route_def.handler,
                        metric_name,
                        self.metrics,
                        tags
                    )
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
