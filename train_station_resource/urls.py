from django.urls import path, include
from rest_framework import routers

from .views import (
    StationViewSet,
    RouteViewSet,
    TrainTypeViewSet,
    TrainViewSet,
    CrewViewSet,
    TripViewSet,
    OrderViewSet,
)

