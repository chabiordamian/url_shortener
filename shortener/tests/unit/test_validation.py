from unittest import TestCase

from shortener.validation import InvalidURL, validate_original_url


class URLValidationTests(TestCase):
    def test_accepts_http_and_https(self) -> None:
        for scheme in ('http', 'https'):
            with self.subTest(scheme=scheme):
                validate_original_url(f'{scheme}://example.com/very-very/long/url/even-longer')

    def test_rejects_invalid_or_unsupported_urls(self) -> None:
        for url in ('', 'not-a-url', 'example.com/path', 'ftp://example.com/file',
                    'javascript:alert(1)', 'http://', ' http://example.com/path',
                    'http://example.com/a\nb'):
            with self.subTest(url=url), self.assertRaises(InvalidURL):
                validate_original_url(url)

    def test_enforces_length_limit(self) -> None:
        prefix = 'http://example.com/'
        longest_url = prefix + 'a' * (2048 - len(prefix))
        validate_original_url(longest_url)
        with self.assertRaises(InvalidURL):
            validate_original_url(longest_url + 'a')
