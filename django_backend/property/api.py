from datetime import datetime

from django.http import JsonResponse
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from .serializers import PropertySerializer, ReservationSerializer

from .models import Property, Reservation

from .permissions import IsAuthenticatedOrReadOnly

from .exception import InvalidPropertyIDException, InvalidReservationException


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
        properties = Property.objects.all().order_by('-created_at')

        bathroom = request.query_params.get('bathroomCount')
        guest = request.query_params.get('guestCount')
        room = request.query_params.get('roomCount')
        category = request.query_params.get('category')
        location = request.query_params.get('locationValue')
        start_date = request.query_params.get('startDate')
        end_date = request.query_params.get('endDate')

        if start_date and end_date:

            start_date = start_date.replace('T', ' ').split()[0]
            format_start_date = datetime.strptime(start_date, '%Y-%m-%d')
            iso_start_date = format_start_date.isoformat()

            end_date = end_date.replace('T', ' ').split()[0]
            format_end_date = datetime.strptime(end_date, '%Y-%m-%d')
            iso_end_date = format_end_date.isoformat()

            exact_matches = Reservation.objects.filter(start_date=iso_start_date) | Reservation.objects.filter(
                end_date=iso_end_date)
            overlap_matches = Reservation.objects.filter(start_date__lte=iso_end_date, end_date__gte=iso_start_date)
            all_matches = []

            for reservation in exact_matches | overlap_matches:
                all_matches.append(reservation.property_id)

            properties = properties.exclude(id__in=all_matches)

        if bathroom:
            properties = properties.filter(bathrooms__gte=bathroom)

        if guest:
            properties = properties.filter(guests__gte=bathroom)

        if room:
            properties = properties.filter(bedrooms__gte=room)

        if category:
            properties = properties.filter(category=category)

        if location:
            properties = properties.filter(country_code=location)

        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PropertyByIdAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk):
        property = Property.objects.get(pk=pk)
        serializer = PropertySerializer(property)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            property = Property.objects.get(pk=pk)
            property.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Property.DoesNotExist:
            raise InvalidPropertyIDException()


class PropertyByUserAPIView(APIView):
    def get(self, request):
        property = Property.objects.filter(landlord=request.user).order_by('-created_at')
        serializer = PropertySerializer(property, many=True)
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

        start_date = datetime.fromisoformat(data["start_date"])
        data["start_date"] = start_date.astimezone(timezone.get_default_timezone())

        end_date = datetime.fromisoformat(data["end_date"])
        data["end_date"] = end_date.astimezone(timezone.get_default_timezone())

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
