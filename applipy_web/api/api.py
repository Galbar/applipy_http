from typing import List

from applipy_web.api.url import UrlFormatter
from applipy_web.api.view import View
from applipy_web.api.route import Route


class ApiName(str):
    ...


class Api:

    HTTP_METHODS = ('GET', 'HEAD', 'POST', 'PUT', 'DELETE',
                    'CONNECT', 'OPTIONS', 'TRACE', 'PATCH')

    _url_formatter: UrlFormatter
    _routes: List[View]

    def __init__(self, url_formatter: UrlFormatter,
                 routes: List[View]) -> None:
        self._url_formatter = url_formatter
        self._routes = routes

    def get_routes(self) -> List[Route]:
        routes = []

        for view in self._routes:
            formatted_path = self._url_formatter.format(view.path())
            for method in self.HTTP_METHODS:
                func = getattr(view, method.lower())
                if not getattr(func, '_view_method_disabled', False):
                    cors_config = getattr(func,
                                          '_cors_config',
                                          view.global_cors_config)
                    routes.append(Route(method,
                                        formatted_path,
                                        func,
                                        cors_config))

        return routes
