from .models import ShortURL
from .repository import ShortURLRepository


class DjangoShortURLRepository(ShortURLRepository):
    def try_add(self, *, url: str, short_code: str) -> bool:
        _, created = ShortURL.objects.get_or_create(
            short_code=short_code,
            defaults={"url": url},
        )
        return created

    def get_original_url(self, short_code: str) -> str | None:
        try:
            stored = ShortURL.objects.get(short_code=short_code)
        except ShortURL.DoesNotExist:
            return None
        return stored.url
