
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import mixins, viewsets
from src.api.dogs import serializers
from src.core.models import Bread, Image
from rest_framework.parsers import MultiPartParser, JSONParser

from rest_framework.response import Response

from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {"code": status_code, "data": data, "count": len(data) if isinstance(data, list) else 1}
        return super().render(response, accepted_media_type, renderer_context)

class BreadViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Bread.objects.all()
    serializer_class = serializers.BreadSerializer
    renderer_classes = [CustomJSONRenderer]

class ImageViewset( 
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Image.objects.all()
    parser_classes = (JSONParser, MultiPartParser,)
    serializer_class = serializers.ImageSerializer

    # Issue with swagger to generate the upload file button. Use default django form instead
    # https://github.com/marcgibbons/django-rest-swagger/issues/647
    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        image = Image(
            file=file,
            type=file.content_type,
            name=file.name,
            size=file.size
        )

        bread = Bread.objects.filter(id=request.data.get('bread')).first()
        if bread:
            image.bread = bread

        image.save()
        return Response(status=status.HTTP_201_CREATED, data={"id": image.id})
