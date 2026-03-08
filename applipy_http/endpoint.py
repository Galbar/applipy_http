import typing as T

from aiohttp import web

from applipy_http.types import CorsConfig, Context

_EndpointSelf = T.TypeVar('_EndpointSelf', bound='Endpoint')
EndpointMethod = T.Callable[[_EndpointSelf, web.Request, Context], T.Coroutine[T.Any, T.Any, web.StreamResponse]]


def _disabled(
        func: EndpointMethod
) -> EndpointMethod:
    async def wrapper(
        self,
        request: web.Request,
        context: Context
    ) -> web.StreamResponse:
        return await func(self, request, context)

    setattr(wrapper, '_endpoint_method_disabled', True)
    return wrapper


class Endpoint:

    global_cors_config: CorsConfig = {}

    @_disabled
    async def get(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise NotImplementedError()

    @_disabled
    async def head(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise NotImplementedError()

    @_disabled
    async def post(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise NotImplementedError()

    @_disabled
    async def put(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise NotImplementedError()

    @_disabled
    async def delete(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise NotImplementedError()

    @_disabled
    async def connect(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise NotImplementedError()

    @_disabled
    async def options(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise NotImplementedError()

    @_disabled
    async def trace(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise NotImplementedError()

    @_disabled
    async def patch(self, request: web.Request, context: Context) -> web.StreamResponse:
        raise NotImplementedError()

    def path(self) -> str:
        raise NotImplementedError()
