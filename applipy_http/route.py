from applipy_http.types import CorsConfig, EndpointHandler


class Route:
    method: str
    path: str
    handler: EndpointHandler
    cors_config: CorsConfig

    def __init__(self, method: str,
                 path: str,
                 handler: EndpointHandler,
                 cors_config: CorsConfig):
        self.method = method
        self.path = path
        self.handler = handler
        self.cors_config = cors_config
