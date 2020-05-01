from typing import Awaitable

from aiohttp import web

from applipy_web.api.view import ViewMethod, CorsConfig


def cors_config(config: CorsConfig) -> ViewMethod:
    def func_handler(func: ViewMethod) -> ViewMethod:
        async def wrapper(
            request: web.Request
        ) -> Awaitable[web.StreamResponse]:
            return await func(request)

        wrapper._cors_config = config

        return wrapper

    return func_handler
