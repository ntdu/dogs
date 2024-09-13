from rest_framework import serializers

from src.core.models import Bread


class BreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = "__all__"


class BreadDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bread
        fields = "__all__"
        read_only_fields = ("images",)
