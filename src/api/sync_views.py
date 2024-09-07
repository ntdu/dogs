
from rest_framework.views import APIView
from rest_framework.response import Response

class Sync(APIView):
    def post(self, request):
        return Response({
            'message': 'Hello, World!'
        })
