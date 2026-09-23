import json
from unittest.mock import patch

from django.test import TestCase

from shortener.models import ShortURL


EXAMPLE_URL = 'http://example.com/very-very/long/url/even-longer'


class ShortenURLAPITests(TestCase):
    def test_returns_short_url_using_request_host_and_scheme(self) -> None:
        with patch('shortener.services.generate_short_code', return_value='Ab12Cd34'):
            response = self.client.post(
                '/api/urls/', data=json.dumps({'url': EXAMPLE_URL}),
                content_type='application/json', secure=True, HTTP_HOST='localhost:8443',
            )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'short_url': 'https://localhost:8443/shrt/Ab12Cd34/'})
        self.assertEqual(ShortURL.objects.get(short_code='Ab12Cd34').url, EXAMPLE_URL)

    def test_invalid_payload_returns_field_error_without_saving(self) -> None:
        payloads: list[dict[str, object]] = [
            {}, {'url': ''}, {'url': None}, {'url': 'not-a-url'},
            {'url': 'ftp://example.com/file'}, {'url': ['http://example.com']},
            {'url': 'http://example.com/' + 'a' * 2048},
        ]
        for payload in payloads:
            with self.subTest(payload=payload):
                response = self.client.post(
                    '/api/urls/', data=json.dumps(payload), content_type='application/json',
                )
                self.assertEqual(response.status_code, 400)
                self.assertIn('url', response.json())
        self.assertEqual(ShortURL.objects.count(), 0)

    def test_exhausted_collisions_return_503(self) -> None:
        ShortURL.objects.create(url=EXAMPLE_URL, short_code='Ab12Cd34')
        with patch('shortener.services.generate_short_code', return_value='Ab12Cd34'):
            response = self.client.post(
                '/api/urls/', data=json.dumps({'url': EXAMPLE_URL}),
                content_type='application/json',
            )

        self.assertEqual(response.status_code, 503)
        self.assertIn('detail', response.json())
        self.assertEqual(ShortURL.objects.count(), 1)


class ResolveURLAPITests(TestCase):
    def test_returns_original_url_as_json_without_redirect(self) -> None:
        ShortURL.objects.create(url=EXAMPLE_URL, short_code='Ab12Cd34')

        response = self.client.get('/shrt/Ab12Cd34/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertEqual(response.json(), {'url': EXAMPLE_URL})
        self.assertNotIn('Location', response)

    def test_unknown_code_returns_404(self) -> None:
        response = self.client.get('/shrt/unknown/')

        self.assertEqual(response.status_code, 404)
