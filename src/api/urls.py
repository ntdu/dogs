from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.api import sync_views
from src.api.dogs import views

router = DefaultRouter()
router.register('breads', views.BreadViewset, basename='breads')
router.register('images', views.ImageViewset, basename='images')

urlpatterns = [
    path('', include(router.urls)),
    path('sync', sync_views.Sync.as_view(), name='sync'),
]
