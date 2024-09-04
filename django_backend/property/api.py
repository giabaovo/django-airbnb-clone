from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PropertySerializer

from .models import Property

from .permissions import IsAuthenticatedOrReadOnly


class PropertyAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        data = request.data
        data['price_per_night'] = int(data['price_per_night'])

        serializer = PropertySerializer(data=data)
        if serializer.is_valid():
            serializer.save(landlord=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        property = Property.objects.all().order_by('-created_at')
        serializer = PropertySerializer(property, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
