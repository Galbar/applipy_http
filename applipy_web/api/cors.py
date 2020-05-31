import typing as T

from aiohttp import web

from applipy_web.types import ViewMethod, CorsConfig, Context


def cors_config(config: CorsConfig) -> T.Callable[[ViewMethod], ViewMethod]:
    def func_handler(func: ViewMethod) -> ViewMethod:
        async def wrapper(
            request: web.Request,
            context: Context
        ) -> T.Awaitable[web.StreamResponse]:
            return await func(request, context)

        wrapper._cors_config = config

        return wrapper

    return func_handler
