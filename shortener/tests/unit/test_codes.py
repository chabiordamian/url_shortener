from unittest import TestCase
from unittest.mock import call, patch

from shortener.codes import generate_short_code


class GenerateCodeTests(TestCase):
    def test_chooses_eight_characters_from_alphanumeric_alphabet(self) -> None:
        alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        with patch('shortener.codes.secrets.choice', side_effect='aZ09bY18') as choose:
            result = generate_short_code()

        self.assertEqual(result, 'aZ09bY18')
        self.assertEqual(choose.call_args_list, [call(alphabet)] * 8)
