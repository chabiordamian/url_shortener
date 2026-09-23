import secrets
import string


CODE_LENGTH = 8
CODE_ALPHABET = string.ascii_letters + string.digits


def generate_short_code() -> str:
    return ''.join(secrets.choice(CODE_ALPHABET) for _ in range(CODE_LENGTH))
