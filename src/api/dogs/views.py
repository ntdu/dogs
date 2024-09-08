from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from src.api.dogs import serializers
from src.api.dogs.filters import BreadFilter
from src.api.dogs.tasks import sync_breads
from src.core.models import Bread, Image


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        renderer_context["response"].status_code = status.HTTP_200_OK
        response = {
            "code": status_code,
            "count": len(data) if isinstance(data, list) else 0,
            "data": data,
        }
        return super().render(response, accepted_media_type, renderer_context)


class BreadViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.BreadSerializer
    renderer_classes = [CustomJSONRenderer]
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = BreadFilter
    search_fields = ("name",)
    ordering_fields = (
        "id",
        "name",
    )
    ordering = ("id",)

    def get_queryset(self):
        queryset = Bread.objects.all()
        if self.action == "retrieve":
            queryset = queryset.prefetch_related("images")
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.BreadDetailSerializer
        elif self.action in (
            "attach_image",
            "sync_breads",
        ):
            return None
        return serializers.BreadSerializer

    @action(detail=True, methods=["patch"], url_path="attach_image/(?P<image_id>[^/.]+)")
    def attach_image(self, request, pk=None, image_id=None):
        bread = self.get_object()
        if not image_id:
            return Response(
                {"detail": "No image ID was provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            image = Image.objects.get(id=image_id)
        except Image.DoesNotExist:
            return Response({"detail": "Image not found."}, status=status.HTTP_404_NOT_FOUND)
        image.bread = bread
        image.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def sync_breads(self, request):
        sync_breads.apply_async()

        return Response({"message": "Started syncing breads."})


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
    serializer_class = serializers.ImageSerializer
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
