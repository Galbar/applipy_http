class Version:
    MAJOR: str = '0'
    MINOR: str = '1'
    PATCH: str = '0'

    VERSION: str = '.'.join((MAJOR, MINOR))
    RELEASE: str = '.'.join((MAJOR, MINOR, PATCH))


__version__ = Version.RELEASE


__all__ = [
    'Api',
    'CorsConfig',
    'UrlFormatter',
    'VersionedUrlFormatter',
    'View',
    'WebHandle',
    'WebModule',
    'cors_config',
]


try:
    from applipy_web.handle import WebHandle
    from applipy_web.api.api import Api
    from applipy_web.api.url import UrlFormatter, VersionedUrlFormatter
    from applipy_web.api.view import View
    from applipy_web.module import WebModule
    from applipy_web.api.cors import CorsConfig, cors_config
except ImportError as e:
    raise ImportError(*e.args, Version, name=e.name, path=e.path)
