from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from src.core.models import Bread, Image
from src.utils.handler import CustomJSONRenderer

from .filters import BreadFilter
from .serializers import BreadDetailSerializer, BreadSerializer
from .tasks import sync_breads


class BreadViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = BreadSerializer
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
            return BreadDetailSerializer
        elif self.action in (
            "attach_image",
            "sync_breads",
        ):
            return None
        return BreadSerializer

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
        return Response({"message": "Success"})

    @action(detail=False, methods=["post"])
    def sync_breads(self, request):

        sync_breads.apply_async()

        return Response({"message": "Started syncing breads."})
