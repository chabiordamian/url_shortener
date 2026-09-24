from typing import Protocol


class ShortURLRepository(Protocol):
    def try_add(self, *, url: str, short_code: str) -> bool: ...

    def get_original_url(self, short_code: str) -> str | None: ...
