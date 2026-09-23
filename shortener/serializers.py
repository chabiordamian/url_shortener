from rest_framework import serializers

from .validation import InvalidURL, MAX_URL_LENGTH, validate_original_url


class ShortenURLSerializer(serializers.Serializer[dict[str, str]]):
    url = serializers.CharField(max_length=MAX_URL_LENGTH, trim_whitespace=False)

    def validate_url(self, value: str) -> str:
        try:
            validate_original_url(value)
        except InvalidURL as exc:
            raise serializers.ValidationError(str(exc)) from exc
        return value
