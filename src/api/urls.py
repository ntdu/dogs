from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.api import sync_views
from src.api.dogs import views

router = DefaultRouter()
router.register('breads', views.BreadViewset, basename='breads')

urlpatterns = [
    # path('', sync_views.Sync.as_view(), name='sync'),
    path('', include(router.urls)),
]
