from .models import ShortURL
from .repository import ShortURLRepository


class DjangoShortURLRepository(ShortURLRepository):
    def add(self, *, url: str, short_code: str) -> None:
        ShortURL.objects.create(url=url, short_code=short_code)

    def get_original_url(self, short_code: str) -> str | None:
        try:
            stored = ShortURL.objects.get(short_code=short_code)
        except ShortURL.DoesNotExist:
            return None
        return stored.url
