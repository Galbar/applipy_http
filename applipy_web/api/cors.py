import typing as T

from aiohttp import web

from applipy_web.types import ViewMethod, CorsConfig, Context
from applipy_web.api.view import View


def cors_config(config: CorsConfig) -> T.Callable[[ViewMethod], ViewMethod]:
    def func_handler(func: ViewMethod) -> ViewMethod:
        async def wrapper(
            self: View,
            request: web.Request,
            context: Context
        ) -> T.Awaitable[web.StreamResponse]:
            return await func(self, request, context)

        wrapper._cors_config = config

        return wrapper

    return func_handler
