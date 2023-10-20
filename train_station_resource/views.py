from django.db.models import Count, F
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from drf_spectacular.utils import (
    extend_schema,
    OpenApiTypes,
    OpenApiParameter,
    OpenApiExample,
)

from .serializers import (
    StationSerializer,
    RouteSerializer,
    RouteListSerializer,
    CrewSerializer,
    TrainTypeSerializer,
    TrainSerializer,
    TrainListSerializer,
    TrainImageSerializer,
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
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name"]
    filterset_fields = ["train_type"]

    def get_serializer_class(self):
        if self.action == "list":
            return TrainListSerializer

        if self.action == "retrieve":
            return TrainDetailSerialize

        if self.action == "upload_image":
            return TrainImageSerializer

        return TrainSerializer

    @action(
        methods=["post"],
        detail=True,
    )
    def upload_image(self, request, pk=None):
        train = self.get_object()
        serializer = self.get_serializer(train, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="search",
                description="Search trains by their name",
                type=str,
                required=False,
                examples=[
                    OpenApiExample(
                        "Example1",
                        description="Search by Train1 name",
                        value="Train1"
                    ),
                    OpenApiExample(
                        "Example2",
                        description="Search by Train2 name",
                        value="Train2"
                    )
                ]
            ),
            OpenApiParameter(
                name="train_type",
                description="Filter trains by train type id",
                type=int,
                required=False,
                examples=[
                    OpenApiExample(
                        "Example1",
                        description="Filter trains by id 2",
                        value=2
                    ),
                    OpenApiExample(
                        "Example2",
                        description="Filter trains by id 3",
                        value=3
                    )
                ]
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CrewViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.select_related(
        "train",
        "route__source",
        "train__train_type",
    ).prefetch_related(
        "crew", "tickets"
    ).annotate(available_tickets=(
        F("train__cargo_num") * F("train__seats_in_cargo")
        - Count("tickets")
    ))
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["train", "route__source"]

    def get_serializer_class(self):
        if self.action == "list":
            return TripListSerializer
        if self.action == "retrieve":
            return TripDetailSerializer

        return TripSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="train",
                description="Filter trips by train id",
                type=int,
                required=False,
                examples=[
                    OpenApiExample(
                        "Example1",
                        description="Filter by train id 1",
                        value=1
                    ),
                    OpenApiExample(
                        "Example2",
                        description="Train by train id 2",
                        value=2
                    )
                ]
            ),
            OpenApiParameter(
                name="route__source",
                description="Filter trips by route source id",
                type=int,
                required=False,
                examples=[
                    OpenApiExample(
                        "Example1",
                        description="Filter by route source id 1",
                        value=1
                    ),
                    OpenApiExample(
                        "Example2",
                        description="Filter by route source id 2",
                        value=2
                    )
                ]
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.prefetch_related(
        "tickets__trip__train" "tickets__trip__route__station"
    )
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["tickets__trip__route"]
    ordering_fields = ["created_at"]

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="tickets__trip__route",
                description=(
                    "Filter orders by tickets trip route id"
                ),
                type=int,
                required=False,
                examples=[
                    OpenApiExample(
                        "Example1",
                        description="Enter route id",
                        value=1
                    )
                ]
            ),
            OpenApiParameter(
                name="ordering",
                description=(
                    "Ordering orders in ascending & descending order"
                    " default is descending"
                ),
                required=False,
                type=str,
                examples=[
                    OpenApiExample(
                        "Example1",
                        description="Filtering in ascending order",
                        value="created_at"
                    ),
                    OpenApiExample(
                        "Example2",
                        description="Filtering in descending order",
                        value="-created_at"
                    )
                ]
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)