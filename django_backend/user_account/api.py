from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User

from .serializers import UserSerializer


class UserAPI(APIView):
    def get(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
