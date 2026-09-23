from dataclasses import dataclass

from .codes import generate_short_code
from .repository import ShortCodeAlreadyExists, ShortURLRepository
from .validation import validate_original_url


MAX_CODE_ATTEMPTS = 5


@dataclass(frozen=True)
class CreatedShortURL:
    short_code: str


@dataclass(frozen=True)
class ResolvedShortURL:
    original_url: str


class ShortURLNotFound(Exception):
    """No URL is stored for the requested short code."""


class CodeGenerationError(Exception):
    """No unused short code was generated within the allowed number of attempts."""


def create_short_url(url: str, repository: ShortURLRepository) -> CreatedShortURL:
    validate_original_url(url)
    for _ in range(MAX_CODE_ATTEMPTS):
        short_code = generate_short_code()
        try:
            repository.insert(url=url, short_code=short_code)
        except ShortCodeAlreadyExists:
            continue
        else:
            return CreatedShortURL(short_code=short_code)

    raise CodeGenerationError('Could not generate an unused short code.')


def resolve_short_url(short_code: str, repository: ShortURLRepository) -> ResolvedShortURL:
    original_url = repository.get_original_url(short_code)
    if original_url is None:
        raise ShortURLNotFound(short_code)
    return ResolvedShortURL(original_url=original_url)
