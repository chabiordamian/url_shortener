from dataclasses import dataclass

from .codes import generate_short_code
from .repository import ShortURLRepository
from .validation import validate_original_url


@dataclass(frozen=True)
class CreatedShortURL:
    short_code: str


class ShortURLNotFound(Exception):
    pass


def create_short_url(url: str, repository: ShortURLRepository) -> CreatedShortURL:
    validate_original_url(url)
    short_code = generate_short_code()
    # For simplicity, a short code collision is handled by the database uniqueness constraint.
    repository.add(url=url, short_code=short_code)
    return CreatedShortURL(short_code=short_code)


def resolve_short_url(short_code: str, repository: ShortURLRepository) -> str:
    original_url = repository.get_original_url(short_code)
    if original_url is None:
        raise ShortURLNotFound(short_code)
    return original_url
