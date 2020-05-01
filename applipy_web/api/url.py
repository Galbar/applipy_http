class UrlFormatter:

    def format(self, path: str) -> str:
        return path


class VersionedUrlFormatter(UrlFormatter):
    _version: str

    def __init__(self, version: str) -> None:
        self._version = version

    def format(self, path: str) -> str:
        return f'/{self._version}{path}'
