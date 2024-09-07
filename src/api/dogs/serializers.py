from rest_framework import serializers
from src.core.models import Bread, Image

class BreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    url = serializers.URLField(read_only=True)
    type = serializers.CharField(read_only=True)
    size = serializers.IntegerField(read_only=True)
    class Meta:
        model = Image
        fields = '__all__'


class BreadDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Bread
        fields = '__all__'
        