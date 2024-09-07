from rest_framework import serializers
from src.core.models import Bread

class BreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = '__all__'
        # exclude = ('watchlist',)