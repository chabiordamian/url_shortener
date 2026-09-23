from unittest.mock import patch

from django.db import IntegrityError
from django.test import TestCase

from shortener.django_repository import DjangoShortURLRepository
from shortener.repository import ShortCodeAlreadyExists


EXAMPLE_URL = 'http://example.com/very-very/long/url/even-longer'


class DjangoShortURLRepositoryTests(TestCase):
    def setUp(self) -> None:
        self.repository = DjangoShortURLRepository()

    def test_stores_and_returns_original_url(self) -> None:
        self.repository.insert(url=EXAMPLE_URL, short_code='Ab12Cd34')

        self.assertEqual(self.repository.get_original_url('Ab12Cd34'), EXAMPLE_URL)

    def test_unknown_code_returns_none(self) -> None:
        self.assertIsNone(self.repository.get_original_url('unknown'))

    def test_translates_collision_and_keeps_connection_usable(self) -> None:
        self.repository.insert(url=EXAMPLE_URL, short_code='Ab12Cd34')

        with self.assertRaises(ShortCodeAlreadyExists):
            self.repository.insert(url=EXAMPLE_URL + '?other=1', short_code='Ab12Cd34')

        self.repository.insert(url=EXAMPLE_URL, short_code='Ef56Gh78')
        self.assertEqual(self.repository.get_original_url('Ab12Cd34'), EXAMPLE_URL)
        self.assertEqual(self.repository.get_original_url('Ef56Gh78'), EXAMPLE_URL)

    def test_database_failure_is_not_translated_to_code_collision(self) -> None:
        self.repository.insert(url=EXAMPLE_URL, short_code='Ab12Cd34')
        error = IntegrityError('Unrelated database constraint')

        with patch('shortener.django_repository.connection.cursor', side_effect=error):
            with self.assertRaises(IntegrityError) as raised:
                self.repository.insert(url=EXAMPLE_URL, short_code='Ab12Cd34')

        self.assertIs(raised.exception, error)
