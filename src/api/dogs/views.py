
from rest_framework import mixins, viewsets
from src.api.dogs import serializers
from src.core.models import Bread

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
