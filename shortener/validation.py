from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


MAX_URL_LENGTH = 2048
_http_url_validator = URLValidator(schemes=["http", "https"])


class InvalidURL(ValueError):
    pass


def validate_original_url(url: str) -> None:
    if len(url) > MAX_URL_LENGTH:
        raise InvalidURL(f"URL must contain at most {MAX_URL_LENGTH} characters.")
    try:
        _http_url_validator(url)
    except ValidationError as exc:
        raise InvalidURL("Enter a valid HTTP or HTTPS URL.") from exc
