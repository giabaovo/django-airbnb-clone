from rest_framework import serializers

from .models import Property

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
