from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import (
    Station,
    Route,
    Trip,
    Crew,
    TrainType,
    Train,
    Order,
    Ticket,
)


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"

