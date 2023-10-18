from django.db.models import Count, F

from rest_framework import viewsets, generics, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from .serializers import (
    StationSerializer,
    RouteSerializer,
    RouteListSerializer,
    CrewSerializer,
    TrainTypeSerializer,
    TrainSerializer,
    TrainListSerializer,
    TrainDetailSerialize,
    TripSerializer,
    TripListSerializer,
    TripDetailSerializer,
    OrderSerializer,
    OrderListSerializer,
)

from .models import (
    Station,
    Route,
    Crew,
    TrainType,
    Train,
    Trip,
    Order,
)


class StationViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Route.objects.select_related(
        "source", "destination"
    )
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        return RouteSerializer


class TrainTypeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = TrainType.objects.all()
    serializer_class = TrainTypeSerializer


class TrainViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Train.objects.select_related(
        "train_type"
    )
    serializer_class = TrainSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer

        if self.action == "retrieve":
            return TrainDetailSerialize

        return TrainSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.select_related(
        "train",
        "route__source",
        "route__destination",
        "train__train_type",
    ).prefetch_related(
        "crew", "tickets"
    ).annotate(available_tickets=(
        F("train__cargo_num") * F("train__seats_in_cargo")
        - Count("tickets")
    ))
    serializer_class = TripSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TripListSerializer
        if self.action == "retrieve":
            return TripDetailSerializer

        return TripSerializer


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    pass
