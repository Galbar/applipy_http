import logging

from aiohttp import web

from applipy import Config, LoggingModule, MetricsModule, Module, with_names

from applipy_web.handle import WebConfig, WebHandle


def _app_runner_wrapper(
        app: web.Application,
        logger: logging.Logger
) -> web.AppRunner:
    return web.AppRunner(app, logger=logger)


class WebModule(Module):

    def __init__(self, config: Config):
        self.config = config

    def configure(self, bind, register):
        webapp_names = self._get_webapp_names()

        for name in webapp_names:
            host = self._get_property(name, 'host')
            port = self._get_property(name, 'port')
            bind(web.Application, name=name)
            bind(web.AppRunner,
                 with_names(_app_runner_wrapper, {'app': name}),
                 name=name)
            bind(WebConfig, WebConfig(name, host, port), name=name)

            register(with_names(WebHandle, {'web_app_runner': name,
                                            'apis': name,
                                            'config': name}))

    def _get_webapp_names(self):
        names = set()
        for key in self.config.keys():
            if key.startswith('web.'):
                parts = key.split('.')
                if len(parts) == 3:
                    names.add(parts[1])
                elif len(parts) == 2:
                    names.add(None)

        return names

    def _get_property(self, name, prop):
        if name is None:
            infix = ''
        else:
            infix = f'.{name}'
        return self.config.get(f'web{infix}.{prop}')

    @classmethod
    def depends_on(cls):
        return (LoggingModule, MetricsModule)
