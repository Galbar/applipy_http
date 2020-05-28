from typing import Callable, Optional, Awaitable, Dict

from aiohttp import web

from applipy_web.types import CorsConfig, ViewMethod


def _disabled(
        func: ViewMethod
) -> ViewMethod:
    async def wrapper(
        request: web.Request
    ) -> web.StreamResponse:
        return await func(request)

    wrapper._view_method_disabled = True
    return wrapper


class View:

    cors_config: Optional[CorsConfig] = None

    @_disabled
    async def get(self, request: web.Request) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def head(self, request: web.Request) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def post(self, request: web.Request) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def put(self, request: web.Request) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def delete(self, request: web.Request) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def connect(self, request: web.Request) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def options(self, request: web.Request) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def trace(self, request: web.Request) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    @_disabled
    async def patch(self, request: web.Request) -> web.StreamResponse:
        raise web.HTTPMethodNotAllowed()

    def path(self) -> str:
        raise NotImplementedError()
