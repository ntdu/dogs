from rest_framework import generics
from rest_framework.response import Response

from src.api.dogs.tasks import sync_breads


class Sync(generics.CreateAPIView):
    def post(self, request):
        # sync_breads.apply_async()
        sync_breads()

        return Response({"data": "Hello, World!", "message": "Hello, World!"})
