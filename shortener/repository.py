from typing import Protocol


class ShortCodeAlreadyExists(Exception):
    pass


class ShortURLRepository(Protocol):
    def add(self, *, url: str, short_code: str) -> None:
        ...

    def get_original_url(self, short_code: str) -> str | None:
        ...
