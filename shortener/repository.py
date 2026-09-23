from typing import Protocol


class ShortCodeAlreadyExists(Exception):
    """The short code is already assigned to a URL."""


class ShortURLRepository(Protocol):
    def insert(self, *, url: str, short_code: str) -> None:
        """Save a new mapping, raising ShortCodeAlreadyExists for a duplicate code."""
        ...

    def get_original_url(self, short_code: str) -> str | None:
        """Return the original URL, or None if the code does not exist."""
        ...
