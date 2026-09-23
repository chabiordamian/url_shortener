from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def hello_world(request: Request) -> Response:
    return Response({'message': 'Hello world'})
