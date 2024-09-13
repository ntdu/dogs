from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from src.api.image.serializers import ImageSerializer
from src.core.models import Bread, Image
from src.utils.handler import CustomJSONRenderer


@extend_schema(tags=["Images"])
class ImageViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Image.objects.all()
    parser_classes = (
        JSONParser,
        MultiPartParser,
    )
    serializer_class = ImageSerializer
    renderer_classes = [CustomJSONRenderer]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    filterset_fields = ("name",)
    search_fields = (
        "name",
        "bread__name",
    )
    ordering_fields = (
        "id",
        "name",
    )
    ordering = ("id",)

    # Issue with swagger to generate the upload file button. Use default django form instead
    # https://github.com/marcgibbons/django-rest-swagger/issues/647
    def create(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        image = Image(file=file, type=file.content_type, name=file.name, size=file.size)

        bread = Bread.objects.filter(id=request.data.get("bread")).first()
        if bread:
            image.bread = bread

        image.save()
        return Response(status=status.HTTP_201_CREATED, data={"id": image.id})

    @action(detail=True, methods=["get"])
    def display(self, request, pk=None):
        image = self.get_object()
        response = FileResponse(image.file)
        return response

    @action(detail=False, methods=["get"])
    def random_images(self, request):
        images = Image.objects.order_by("?")[:20]
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)
