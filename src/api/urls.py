from django.urls import path, include
from rest_framework.routers import DefaultRouter
from src.api import sync_views

router = DefaultRouter()

urlpatterns = [
    path('', sync_views.Sync.as_view(), name='sync'),
    path('', include(router.urls)),
]
