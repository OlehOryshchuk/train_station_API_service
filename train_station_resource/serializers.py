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
    def validate(self, attrs):
        data = super().validate(attrs)
        Route.validate_route(
            attrs["source"],
            attrs["destination"],
            ValidationError,
        )
        return data

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
            "id",
            "name",
            "cargo_num",
            "seats_in_cargo",
            "train_type",
        ]


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
        ]


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super().validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["cargo"],
            attrs["seat"],
            attrs["trip"].train,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = [
            "id",
            "cargo",
            "seat",
            "trip"
        ]


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(
        many=True, read_only=False, allow_empty=False
    )

    class Meta:
        model = Order
        fields = ["id", "tickets", "created_at"]

    @transaction.atomic
    def create(self, validated_data):
        tickets = validated_data.pop("tickets")
        order = Order.objects.create(**validated_data)

        for ticket in tickets:
            Ticket.objects.create(order=order, **ticket)

        return order


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )
    destination = serializers.SlugRelatedField(
        read_only=True, slug_field="name"
    )


class TrainListSerializer(TrainSerializer):
    train_type_name = serializers.CharField(
        read_only=True, source="train_type.name"
    )

    class Meta:
        model = Train
        fields = [
            "id",
            "name",
            "cargo_num",
            "seats_in_cargo",
            "train_type_name",
            "image",
            "capacity",
        ]


class TrainDetailSerializer(TrainSerializer):
    train_type = TrainTypeSerializer(read_only=True)

    class Meta:
        model = Train
        fields = [
            "id",
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


class TripListSerializer(TripSerializer):
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    route = serializers.SlugRelatedField(
        read_only=True, slug_field="string_repr"
    )
    train_name = serializers.CharField(
        read_only=True, source="train.name"
    )
    train_image = serializers.ImageField(
        source="train.image", read_only=True,
    )
    train_capacity = serializers.IntegerField(
        read_only=True, source="train.capacity"
    )
    available_tickets = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Trip
        fields = [
            "id",
            "crew",
            "route",
            "departure_time",
            "arrival_time",
            "train_name",
            "train_image",
            "train_capacity",
            "available_tickets",
        ]


class TicketTakenPlacesSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ["cargo", "seat"]


class TripDetailSerializer(TripSerializer):
    crew = CrewSerializer(many=True, read_only=True)
    route = RouteListSerializer(read_only=True)
    train = TrainListSerializer(read_only=True)
    taken_places = TicketTakenPlacesSerializer(
        many=True, read_only=True, source="tickets"
    )

    class Meta:
        model = Trip
        fields = [
            "id",
            "route",
            "train",
            "taken_places",
            "departure_time",
            "arrival_time",
            "crew",
        ]


class TicketListSerializer(TicketSerializer):
    trip = TripListSerializer(read_only=True)


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
