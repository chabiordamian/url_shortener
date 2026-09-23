from unittest import TestCase
from unittest.mock import patch

from shortener.repository import ShortCodeAlreadyExists, ShortURLRepository
from shortener.services import (
    CodeGenerationError, CreatedShortURL, ResolvedShortURL, ShortURLNotFound,
    create_short_url, resolve_short_url,
)
from shortener.validation import InvalidURL


EXAMPLE_URL = 'http://example.com/very-very/long/url/even-longer'


class InMemoryShortURLRepository(ShortURLRepository):
    def __init__(self) -> None:
        self.urls: dict[str, str] = {}

    def insert(self, *, url: str, short_code: str) -> None:
        if short_code in self.urls:
            raise ShortCodeAlreadyExists(short_code)
        self.urls[short_code] = url

    def get_original_url(self, short_code: str) -> str | None:
        return self.urls.get(short_code)


class CreateShortURLTests(TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryShortURLRepository()

    def test_creates_separate_short_urls_for_repeated_url(self) -> None:
        with patch('shortener.services.generate_short_code', side_effect=['Ab12Cd34', 'Ef56Gh78']):
            first = create_short_url(EXAMPLE_URL, self.repository)
            second = create_short_url(EXAMPLE_URL, self.repository)

        self.assertEqual(first, CreatedShortURL(short_code='Ab12Cd34'))
        self.assertEqual(second, CreatedShortURL(short_code='Ef56Gh78'))
        self.assertEqual(
            self.repository.urls,
            {'Ab12Cd34': EXAMPLE_URL, 'Ef56Gh78': EXAMPLE_URL},
        )

    def test_retries_collision_without_overwriting_existing_url(self) -> None:
        existing_url = EXAMPLE_URL + '?existing=1'
        self.repository.insert(url=existing_url, short_code='Ab12Cd34')

        with patch('shortener.services.generate_short_code', side_effect=['Ab12Cd34', 'Ef56Gh78']):
            created = create_short_url(EXAMPLE_URL, self.repository)

        self.assertEqual(self.repository.urls['Ab12Cd34'], existing_url)
        self.assertEqual(created.short_code, 'Ef56Gh78')
        self.assertEqual(self.repository.urls['Ef56Gh78'], EXAMPLE_URL)

    def test_can_succeed_on_fifth_attempt(self) -> None:
        self.repository.insert(url=EXAMPLE_URL, short_code='Ab12Cd34')

        with patch(
            'shortener.services.generate_short_code',
            side_effect=['Ab12Cd34'] * 4 + ['Ef56Gh78'],
        ):
            created = create_short_url(EXAMPLE_URL, self.repository)

        self.assertEqual(created.short_code, 'Ef56Gh78')

    def test_raises_after_five_collisions_without_creating_a_record(self) -> None:
        self.repository.insert(url=EXAMPLE_URL, short_code='Ab12Cd34')

        with patch('shortener.services.generate_short_code', return_value='Ab12Cd34') as generate:
            with self.assertRaises(CodeGenerationError):
                create_short_url(EXAMPLE_URL, self.repository)

        self.assertEqual(generate.call_count, 5)
        self.assertEqual(len(self.repository.urls), 1)

    def test_storage_failure_is_not_retried(self) -> None:
        # A matching code must not turn an unrelated failure into a collision.
        self.repository.insert(url=EXAMPLE_URL, short_code='Ab12Cd34')
        error = RuntimeError('Storage unavailable')

        with (
            patch('shortener.services.generate_short_code', return_value='Ab12Cd34') as generate,
            patch.object(self.repository, 'insert', side_effect=error),
        ):
            with self.assertRaises(RuntimeError) as raised:
                create_short_url(EXAMPLE_URL, self.repository)

        self.assertIs(raised.exception, error)
        self.assertEqual(generate.call_count, 1)

    def test_invalid_url_is_rejected_before_generating_or_saving(self) -> None:
        with patch('shortener.services.generate_short_code') as generate:
            with self.assertRaises(InvalidURL):
                create_short_url('ftp://example.com/file', self.repository)

        generate.assert_not_called()
        self.assertEqual(len(self.repository.urls), 0)


class ResolveShortURLTests(TestCase):
    def setUp(self) -> None:
        self.repository = InMemoryShortURLRepository()

    def test_returns_original_url_without_exposing_model(self) -> None:
        self.repository.insert(url=EXAMPLE_URL, short_code='Ab12Cd34')

        self.assertEqual(resolve_short_url('Ab12Cd34', self.repository), ResolvedShortURL(EXAMPLE_URL))

    def test_unknown_code_raises_not_found(self) -> None:
        with self.assertRaises(ShortURLNotFound):
            resolve_short_url('unknown', self.repository)
