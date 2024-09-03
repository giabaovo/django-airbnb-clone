from rest_framework import serializers

from .models import Property


class LocationField(serializers.Field):
    def to_representation(self, value):
        pass

    def to_internal_value(self, data):
        ret = {
            "country": data["label"],
            "country_code": data["value"],
        }
        return ret


class PropertySerializer(serializers.ModelSerializer):
    location = LocationField(source='*')

    class Meta:
        model = Property
        fields = (
            'title',
            'description',
            'price_per_night',
            'bedrooms',
            'bathrooms',
            'guests',
            'image',
            'location'
        )
