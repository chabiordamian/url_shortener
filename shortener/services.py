from dataclasses import dataclass

from .codes import generate_short_code
from .repository import ShortCodeAlreadyExists, ShortURLRepository
from .validation import validate_original_url


MAX_CODE_GENERATION_ATTEMPTS = 3


@dataclass(frozen=True)
class CreatedShortURL:
    short_code: str


class ShortURLNotFound(Exception):
    pass


class ShortCodeGenerationError(Exception):
    pass


def create_short_url(url: str, repository: ShortURLRepository) -> CreatedShortURL:
    validate_original_url(url)

    for _ in range(MAX_CODE_GENERATION_ATTEMPTS):
        short_code = generate_short_code()

        try:
            repository.add(url=url, short_code=short_code)
        except ShortCodeAlreadyExists:
            continue

        return CreatedShortURL(short_code=short_code)

    raise ShortCodeGenerationError


def resolve_short_url(short_code: str, repository: ShortURLRepository) -> str:
    original_url = repository.get_original_url(short_code)
    if original_url is None:
        raise ShortURLNotFound(short_code)
    return original_url