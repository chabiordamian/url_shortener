from django.db import IntegrityError, transaction
from django.test import TestCase

from shortener.django_repository import DjangoShortURLRepository


EXAMPLE_URL = 'http://example.com/very-very/long/url/even-longer'


class DjangoShortURLRepositoryTests(TestCase):
    def setUp(self) -> None:
        self.repository = DjangoShortURLRepository()

    def test_duplicate_code_is_rejected_without_overwriting_url(self) -> None:
        self.repository.add(url=EXAMPLE_URL, short_code='Ab12Cd34')

        with self.assertRaises(IntegrityError), transaction.atomic():
            self.repository.add(url=EXAMPLE_URL + '?other=1', short_code='Ab12Cd34')

        self.assertEqual(self.repository.get_original_url('Ab12Cd34'), EXAMPLE_URL)

    def test_same_url_can_be_stored_under_different_codes(self) -> None:
        self.repository.add(url=EXAMPLE_URL, short_code='Ab12Cd34')
        self.repository.add(url=EXAMPLE_URL, short_code='Ef56Gh78')

        self.assertEqual(self.repository.get_original_url('Ab12Cd34'), EXAMPLE_URL)
        self.assertEqual(self.repository.get_original_url('Ef56Gh78'), EXAMPLE_URL)
