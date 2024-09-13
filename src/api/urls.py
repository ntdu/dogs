from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.api.bread.views import BreadViewset
from src.api.image.views import ImageViewset

router = DefaultRouter()
router.register("breads", BreadViewset, basename="breads")
router.register("images", ImageViewset, basename="images")

urlpatterns = [
    path("v1/", include((router.urls, "api"), namespace="v1")),
]
