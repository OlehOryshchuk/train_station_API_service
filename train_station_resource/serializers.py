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


class TrainTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainType
        fields = "__all__"


class TrainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Train
        fields = [
            "name",
            "cargo_num",
            "seats_in_cargo",
            "train_type",
            "capacity",
        ]


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = [
            "first_name",
            "last_name",
            "full_name",
        ]


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )
    destination = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )


class TrainListSerializer(TrainSerializer):
    train_type = serializers.SlugRelatedField(
        read_only=True, slug_field="name",
    )

    class Meta:
        model = Train
        fields = [
            "name",
            "cargo_num",
            "seats_in_cargo",
            "train_type",
            "image",
        ]


class TrainDetailSerialize(TrainSerializer):
    train_type = TrainTypeSerializer(read_only=True)

    class Meta:
        model = Train
        fields = [
            "name",
            "cargo_num",
            "seats_in_cargo",
            "train_type",
            "image",
        ]


class TrainImageSerializer(TrainSerializer):
    class Meta:
        model = Train
        fields = ["id", "image"]
