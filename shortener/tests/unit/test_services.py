from unittest import TestCase
from unittest.mock import patch

from shortener.repository import ShortURLRepository
from shortener.services import CreatedShortURL, create_short_url
from shortener.validation import InvalidURL


EXAMPLE_URL = 'http://example.com/very-very/long/url/even-longer'


class InMemoryShortURLRepository(ShortURLRepository):
    def __init__(self) -> None:
        self.urls: dict[str, str] = {}

    def add(self, *, url: str, short_code: str) -> None:
        self.urls[short_code] = url

    def get_original_url(self, short_code: str) -> str | None:
        return self.urls.get(short_code)


class CreateShortURLTests(TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryShortURLRepository()

    def test_saves_generated_code_and_returns_result(self) -> None:
        with patch('shortener.services.generate_short_code', return_value='Ab12Cd34') as generate:
            created = create_short_url(EXAMPLE_URL, self.repository)

        self.assertEqual(created, CreatedShortURL(short_code='Ab12Cd34'))
        self.assertEqual(self.repository.urls, {'Ab12Cd34': EXAMPLE_URL})
        generate.assert_called_once_with()

    def test_invalid_url_is_rejected_before_generating_or_saving(self) -> None:
        with patch('shortener.services.generate_short_code') as generate:
            with self.assertRaises(InvalidURL):
                create_short_url('ftp://example.com/file', self.repository)

        generate.assert_not_called()
        self.assertEqual(self.repository.urls, {})
