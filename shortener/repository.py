from typing import Protocol


class ShortURLRepository(Protocol):
    def add(self, *, url: str, short_code: str) -> None:
        """Save a new mapping. Database failures propagate to the caller."""
        ...

    def get_original_url(self, short_code: str) -> str | None:
        """Return the original URL, or None if the code does not exist."""
        ...
