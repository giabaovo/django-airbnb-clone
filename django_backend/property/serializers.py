from rest_framework import serializers

from .models import Property, Reservation

from user_account.serializers import UserSerializer


class LocationField(serializers.Field):
    def to_representation(self, value):
        ret = {
            "label": value.country,
            "value": value.country_code
        }

        return ret

    def to_internal_value(self, data):
        ret = {
            "country": data["label"],
            "country_code": data["value"],
        }
        return ret


class PropertySerializer(serializers.ModelSerializer):
    location = LocationField(source='*')
    landlord = UserSerializer(read_only=True)

    class Meta:
        model = Property
        fields = (
            'id',
            'title',
            'description',
            'price_per_night',
            'bedrooms',
            'bathrooms',
            'guests',
            'image',
            'location',
            'landlord',
            'category',
            'created_at'
        )
        extra_kwargs = {
            'landlord': {'required': False},
            'id': {'required': False},
            'created_at': {'required': False},
        }


class ReservationSerializer(serializers.ModelSerializer):
    property = PropertySerializer(required=False)

    class Meta:
        model = Reservation
        fields = (
            'id',
            'start_date',
            'end_date',
            'property',
            'total_price',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['startDate'] = representation.pop('start_date')
        representation['endDate'] = representation.pop('end_date')
        representation['totalPrice'] = representation.pop('total_price')
        representation['listing'] = representation.pop('property')

        return representation