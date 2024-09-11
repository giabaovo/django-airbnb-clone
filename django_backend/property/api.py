from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from .serializers import PropertySerializer, ReservationSerializer

from .models import Property, Reservation
from user_account.models import User

from .permissions import IsAuthenticatedOrReadOnly

from .exception import InvalidPropertyIDException, InvalidReservationException

import datetime


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


class PropertyByIdAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk):
        property = Property.objects.get(pk=pk)
        serializer = PropertySerializer(property)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFavoritePropertyAPIView(APIView):
    def get(self, request):
        try:
            if not request.user:
                return JsonResponse({'listings': []})
            user_favorite_property = Property.objects.filter(favorited=request.user).values()
            return JsonResponse({'listings': list(user_favorite_property)})
        except Exception as e:
            raise APIException(detail=str(e))


class ToggleFavoritePropertyAPIView(APIView):
    def post(self, request, pk):
        try:
            property = Property.objects.get(pk=pk)

            if request.user in property.favorited.all():
                property.favorited.remove(request.user)
                return Response(status=status.HTTP_200_OK)
            property.favorited.add(request.user)
            return Response(status=status.HTTP_200_OK)
        except Property.DoesNotExist:
            raise InvalidPropertyIDException()
        except Exception as e:
            raise APIException(detail=str(e))


class ReservationByPropertyAPIView(APIView):
    def post(self, request, pk):
        data = request.data

        data["start_date"] = data.pop("startDate")
        data["end_date"] = data.pop("endDate")
        data["total_price"] = data.pop("totalPrice")

        try:
            property = Property.objects.get(pk=data["listingId"])
        except Property.DoesNotExist:
            raise InvalidPropertyIDException()

        serializer = ReservationSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, property=property)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            property = Property.objects.get(pk=pk)
            reservation = Reservation.objects.filter(property=property).order_by('-created_at')
            serializer = ReservationSerializer(reservation, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Property.DoesNotExist:
            raise InvalidPropertyIDException()


class ReservationByUserIdAPIView(APIView):
    def get(self, request):
        try:
            reservation = Reservation.objects.filter(created_by=request.user).order_by('-created_at')
            serializer = ReservationSerializer(reservation, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=str(e))


class ReservationByAuthorAPIView(APIView):
    def get(self, request):
        try:
            reservation = Reservation.objects.filter(property__landlord=request.user).order_by('-created_at')
            serializer = ReservationSerializer(reservation, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException(detail=str(e))


class ReservationAPIView(APIView):
    def delete(self, request, pk):
        try:
            reservation = Reservation.objects.get(pk=pk)
            reservation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Reservation.DoesNotExist:
            raise InvalidReservationException()
