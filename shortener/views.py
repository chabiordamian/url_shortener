from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from .django_repository import DjangoShortURLRepository
from .serializers import ShortenURLSerializer
from .services import (
    CodeGenerationError,
    ShortURLNotFound,
    create_short_url,
    resolve_short_url,
)


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def shorten_url(request: Request) -> Response:
    serializer = ShortenURLSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        created = create_short_url(serializer.validated_data['url'], DjangoShortURLRepository())
    except CodeGenerationError:
        return Response(
            {'detail': 'Could not create a short URL. Please try again.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    path = reverse('resolve-url', kwargs={'short_code': created.short_code})
    return Response(
        {'short_url': request.build_absolute_uri(path)},
        status=status.HTTP_201_CREATED,
    )


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def resolve_url(request: Request, short_code: str) -> Response:
    try:
        resolved = resolve_short_url(short_code, DjangoShortURLRepository())
    except ShortURLNotFound:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'url': resolved.original_url})
