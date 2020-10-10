import aiohttp_cors
from applipy import Module as Module_
from applipy_web import WebModule, Api, View, UrlFormatter, PrefixUrlFormatter, cors_config
from applipy_inject import with_names
from .common import ApplipyProcess
from aiohttp import web
import requests
from logging import Logger


class ViewA(View):

    def __init__(self, logger: Logger):
        self.logger = logger.getChild(self.__class__.__name__)

    async def get(self, request, ctx):
        self.logger.info('GET')
        return web.Response(body='GET Success')

    async def post(self, request, ctx):
        self.logger.info('POST')
        return web.Response(body='POST Success')

    def path(self):
        return '/testA'


class ViewB(View):

    async def put(self, request, ctx):
        return web.Response(body=f'PUT Matched `{request.match_info["var"]}`')

    async def patch(self, request, ctx):
        return web.Response(body=f'PATCH Matched `{request.match_info["var"]}`')

    def path(self):
        return '/testB/{var:.*}'


class ViewC(View):

    global_cors_config = {'*': aiohttp_cors.ResourceOptions(allow_credentials=False, allow_methods=('POST',))}

    @cors_config({'http://localhost:8080': aiohttp_cors.ResourceOptions(allow_methods=('GET',))})
    async def get(self, request, ctx):
        return web.Response(body='GET with cors config')

    async def post(self, request, ctx):
        return web.Response(body='POST with cors config')

    def path(self):
        return '/testC'


class Module(Module_):

    def configure(self, bind, register):
        bind(View, ViewB, name='other')
        bind(UrlFormatter, PrefixUrlFormatter('other'), name='other')
        bind(Api, with_names(Api, 'other'), name='other')

        bind(View, ViewA)
        bind(View, ViewC)
        bind(UrlFormatter)
        bind(Api)

    @classmethod
    def depends_on(cls):
        return WebModule,


def test_applipy_web():
    with ApplipyProcess('./tests/acceptance', 'test_applipy_web') as p:
        with requests.get('http://0.0.0.0:8080/testA') as r:
            assert r.status_code == 200
            assert r.text == 'GET Success'

        with requests.post('http://0.0.0.0:8080/testA') as r:
            assert r.status_code == 200
            assert r.text == 'POST Success'

        with requests.put('http://0.0.0.0:8081/other/testB/foo') as r:
            assert r.status_code == 200
            assert r.text == 'PUT Matched `foo`'

        with requests.patch('http://0.0.0.0:8081/other/testB/bar') as r:
            assert r.status_code == 200
            assert r.text == 'PATCH Matched `bar`'

        with requests.get('http://0.0.0.0:8080/testC') as r:
            # TODO: This does not check CORS functionality
            assert r.status_code == 200
            assert r.text == 'GET with cors config'

        with requests.post('http://0.0.0.0:8080/testC') as r:
            # TODO: This does not check CORS functionality
            assert r.status_code == 200
            assert r.text == 'POST with cors config'

    assert p.returncode == 0
