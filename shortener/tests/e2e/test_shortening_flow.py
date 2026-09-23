import json
from urllib.request import Request, urlopen

from django.test import LiveServerTestCase


class ShorteningFlowTests(LiveServerTestCase):
    def test_shorten_and_resolve_preserves_original_url(self) -> None:
        original_url = 'http://example.com/very-very/long/url/even-longer?lang=pl&page=2#part'
        request = Request(
            self.live_server_url + '/api/urls/',
            data=json.dumps({'url': original_url}).encode(),
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        with urlopen(request, timeout=5) as response:
            self.assertEqual(response.status, 201)
            payload = json.load(response)

        short_url = payload['short_url']
        self.assertIsInstance(short_url, str)
        self.assertTrue(short_url.startswith(self.live_server_url + '/shrt/'))
        with urlopen(short_url, timeout=5) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers.get_content_type(), 'application/json')
            self.assertEqual(json.load(response), {'url': original_url})
