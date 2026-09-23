from django.db import connection

from .models import ShortURL
from .repository import ShortCodeAlreadyExists, ShortURLRepository


class DjangoShortURLRepository(ShortURLRepository):
    def insert(self, *, url: str, short_code: str) -> None:
        table = connection.ops.quote_name(ShortURL._meta.db_table)
        with connection.cursor() as cursor:
            cursor.execute(
                f'INSERT INTO {table} ("url", "short_code") VALUES (%s, %s) '
                'ON CONFLICT ("short_code") DO NOTHING RETURNING "id"',
                [url, short_code],
            )
            inserted = cursor.fetchone() is not None
        if not inserted:
            raise ShortCodeAlreadyExists(short_code)

    def get_original_url(self, short_code: str) -> str | None:
        try:
            stored = ShortURL.objects.get(short_code=short_code)
        except ShortURL.DoesNotExist:
            return None
        return stored.url

