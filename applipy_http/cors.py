import typing as T

from aiohttp import web

from applipy_http.types import CorsConfig, Context
from applipy_http.endpoint import EndpointMethod


def cors_config(config: CorsConfig) -> T.Callable[[EndpointMethod], EndpointMethod]:
    def func_handler(func: EndpointMethod) -> EndpointMethod:
        async def wrapper(
            self,
            request: web.Request,
            context: Context
        ) -> web.StreamResponse:
            return await func(self, request, context)

        setattr(wrapper, '_cors_config', config)
        return wrapper

    return func_handler
