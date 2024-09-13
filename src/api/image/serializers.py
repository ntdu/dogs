from rest_framework import serializers

from src.core.models import Image


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
