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
    pass


class RouteViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class TrainTypeViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    pass


class TrainViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class TripViewSet(viewsets.ModelViewSet):
    pass


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    pass
