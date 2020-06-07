class UrlFormatter:

    def format(self, path: str) -> str:
        return path


class PrefixUrlFormatter(UrlFormatter):
    _version: str

    def __init__(self, prefix: str) -> None:
        self._prefix = prefix

    def format(self, path: str) -> str:
        return f'/{self._prefix}{path}'
