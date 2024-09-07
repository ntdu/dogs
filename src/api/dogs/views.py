
from rest_framework import viewsets
from src.api.dogs import serializers
from src.core.models import Bread

class BreadViewset(viewsets.ModelViewSet):
    queryset = Bread.objects.all()
    serializer_class = serializers.BreadSerializer
