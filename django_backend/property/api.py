from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PropertySerializer


class PropertyAPIView(APIView):
    def post(self, request):
        data = request.data
        data['price_per_night'] = int(data['price_per_night'])

        serializer = PropertySerializer(data=data)
        if serializer.is_valid():
            serializer.save(landlord=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
