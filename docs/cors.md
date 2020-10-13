# CORS

Applipy HTTP uses [ `aiohttp_cors` ](https://github.com/aio-libs/aiohttp-cors)
to allow setting CORS configuration to endpoints.

There are two ways to define the CORS configuration of an endpoints: global and
by HTTP method.


```python
from aiohttp_cors import ResourceOptions
from applipy_http import Endpoint, cors_config


class MyEndpoint(Endpoint):

    # CORS configuration for all HTTP methods of this endpoint
    global_cors_config = {
        '*': ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        ),
    }

    async def get(self, request, ctx):
        ...

    # Override the global configuration with one specific for the POST method
    @cors_config({
        'http://example.org': ResourceOptions(
            allow_credentials=False,
            expose_headers="",
            allow_headers="",
        ),
    })
    async def post(self, request, ctx):
        ...

    def path(self):
        return '/path'
```
