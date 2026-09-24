from django.db import IntegrityError, transaction

from .models import ShortURL
from .repository import ShortCodeAlreadyExists, ShortURLRepository


class DjangoShortURLRepository(ShortURLRepository):
    def add(self, *, url: str, short_code: str) -> None:
        try:
            with transaction.atomic():
                ShortURL.objects.create(url=url, short_code=short_code)
        except IntegrityError as exc:
            raise ShortCodeAlreadyExists(short_code) from exc

    def get_original_url(self, short_code: str) -> str | None:
        try:
            stored = ShortURL.objects.get(short_code=short_code)
        except ShortURL.DoesNotExist:
            return None
        return stored.url
