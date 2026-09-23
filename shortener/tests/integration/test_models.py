from django.db import IntegrityError, transaction
from django.test import TestCase

from shortener.models import ShortURL


class ShortURLModelTests(TestCase):
    def test_duplicate_code_is_rejected_by_database(self) -> None:
        original_url = 'http://example.com/very-very/long/url/even-longer'
        ShortURL.objects.create(url=original_url, code='Ab12Cd34')

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ShortURL.objects.create(url=original_url, code='Ab12Cd34')

    def test_same_url_can_have_multiple_codes(self) -> None:
        original_url = 'http://example.com/very-very/long/url/even-longer'
        ShortURL.objects.create(url=original_url, code='Ab12Cd34')
        ShortURL.objects.create(url=original_url, code='Ef56Gh78')

        self.assertEqual(ShortURL.objects.filter(url=original_url).count(), 2)
