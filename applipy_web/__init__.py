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


from .module import WebModule
from .handle import WebHandle
from .api.api import Api
from .api.url import UrlFormatter, VersionedUrlFormatter
from .api.view import View
from .api.cors import CorsConfig, cors_config
