from typing import Protocol


class ShortCodeAlreadyExists(Exception):
    pass


class ShortURLRepository(Protocol):
    def insert(self, *, url: str, short_code: str) -> None:
        pass

    def get_original_url(self, short_code: str) -> str | None:
        pass
