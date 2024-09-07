
from rest_framework import generics
from rest_framework.response import Response

class Sync(generics.CreateAPIView):
    def post(self, request):
        return Response({
            'data': 'Hello, World!',
            'message': 'Hello, World!'
        })
