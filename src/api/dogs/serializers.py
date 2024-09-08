from rest_framework import serializers

from src.core.models import Bread, Image


class BreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
        read_only_fields = (
            "name",
            "url",
            "type",
            "size",
        )


class BreadDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = "__all__"
        read_only_fields = ("images",)
