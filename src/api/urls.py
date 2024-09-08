from django.urls import include, path
from rest_framework.routers import DefaultRouter

from src.api.dogs import views

router = DefaultRouter()
router.register("breads", views.BreadViewset, basename="breads")
router.register("images", views.ImageViewset, basename="images")

urlpatterns = [
    path("", include(router.urls)),
]
