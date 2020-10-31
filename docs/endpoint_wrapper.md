# Endpoint Wrapper

Applipy implements functionality to intercept all HTTP requests in an API.

This is done by implementing an `applipy_http.EndpointWrapper`.

## EndpointWrapper wrap()

The wrapper implements a method `wrap()` that receives the endpoint handler
method and returns a function that looks the same as the original endpoint
handler. The returned function can be used to wrap the original handler and it
will be used in place of the original handler.

## EndpointWrapper priority

The priority defines when the wrapper is applied relative to other registered
wrappers. The highest the priority, the later it is applied (It will wrap all
the lower priority wrappers).

## Demo

Bellow you can find an implementation that checks that the user is logged in,
adds the user identity to the [`Context`](context.md) and rejects the request
if the user is not logged in:

```python
from applipy_http import EndpointMethod, EndpointWrapper
from myIdentities import TokenStore

class LoginCheck(EndpointWrapper):

    # The `TokenStore` is a class that tells us the user for a given
    # login cookie
    def __init__(self, tokens: TokenStore) -> None:
        self._tokens = tokens

    def wrap(self, method: str, path: str, handler: EndpointMethod) -> EndpointMethod:

        # The handler is an `EndpointMethod`. That means it is a function that for
        # all purposes looks and behaves like a method of the class `Endpoint`.
        # The wraper implements its own `EndpointMethod` substitute that wraps the
        # `handler` and will replace it when a request is made.
        async def wrapper(request: web.Request, ctx: Context) -> web.Response:

            # Get the user identity
            session_token = request.cookies.get('SESSION')
            user_id = 'UNKNOWN'
            if session_token:
                id = self._tokens.get_identity(session_token)
                if id:
                    ctx['user.identity'] = id

            # Return a HTTP Forbidden response if user is not logged in
            if ctx.get('user.identity'):
                return await handler(request, ctx)
            else:
                raise web.HTTPForbidden()

        return wrapper
```

The `EndpointWrapper` is doing two parts of logic:
 - Get user identity from session cookie
 - Allow or deny access to the API based on login status

We might want to have the login logic in other APIs but not the access
controller.

Lucky for us, applipy supports registering multiple `EndpointWrapper` to the
same API and define the order we want them to be applied. Bellow we have the
same logic split in two wrappers and setting their order (priority) so that the
one that checks if the user is logged in is run after the one that retrieves
the identity from the cookie:

```python
from applipy_http import EndpointMethod, EndpointWrapper
from myIdentities import TokenStore

class LoadIdentity(EndpointWrapper):

    # The `TokenStore` is a class that tells us the user for a given
    # login cookie
    def __init__(self, tokens: TokenStore) -> None:
        self._tokens = tokens

    def wrap(self, method: str, path: str, handler: EndpointMethod) -> EndpointMethod:
        async def wrapper(request: web.Request, ctx: Context) -> web.Response:

            # Get the user identity
            session_token = request.cookies.get('SESSION')
            user_id = 'UNKNOWN'
            if session_token:
                id = self._tokens.get_identity(session_token)
                if id:
                    ctx['user.identity'] = id
            return await handler(request, ctx)

        return wrapper

    def priority(self) -> int:
        return 20


class LoginCheck(EndpointWrapper):

    def wrap(self, method: str, path: str, handler: EndpointMethod) -> EndpointMethod:
        async def wrapper(request: web.Request, ctx: Context) -> web.Response:

            # Return a HTTP Forbidden response if user is not logged in
            if ctx.get('user.identity'):
                return await handler(request, ctx)
            else:
                raise web.HTTPForbidden()

        return wrapper

    def priority(self) -> int:
        return 10
```

Now the `EndpointWrapper`s can be registered for various APIs:

```python
class MyModule(Module):

    def configure(self, bind, register):
        ...
        bind(EndpointWrapper, LoadIdentity, name='public')
        bind(with_names(Api, 'public'))

        ...
        bind(EndpointWrapper, LoadIdentity, name='private')
        bind(EndpointWrapper, LoginCheck, name='private')
        bind(with_names(Api, 'private'))
```
