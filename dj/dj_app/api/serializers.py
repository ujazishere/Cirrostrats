from rest_framework.serializers import ModelSerializer
from ..models import Flight, SearchQuery


class PostSerializer(ModelSerializer):
    class Meta:
        model = Flight
        fields = ['gate', 'flight_number', 'scheduled', 'actual']
