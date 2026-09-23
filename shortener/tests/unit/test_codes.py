from unittest import TestCase

from shortener.codes import generate_code


class GenerateCodeTests(TestCase):
    def test_code_has_eight_characters(self) -> None:
        self.assertEqual(len(generate_code()), 8)

    def test_code_contains_only_ascii_letters_and_digits(self) -> None:
        self.assertRegex(generate_code(), r'\A[a-zA-Z0-9]+\Z')
