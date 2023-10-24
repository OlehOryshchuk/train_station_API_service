from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from train_station_resource.serializers import (
    RouteSerializer,
    RouteListSerializer,
)
from .models_create_sample import (
    sample_trip,
    sample_train,
    detail_url,
)
from train_station_resource.models import Trip

TRIP_URL = reverse("train_station:trip-list")


class UnauthenticatedTripApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_method_auth_required(self):
        res = self.client.get(TRIP_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_method_auth_required(self):
        res = self.client.post(TRIP_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_trip_detail_auth_required(self):
        trip = sample_trip(name="Trip1")
        res = self.client.get(detail_url("trip", trip.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_method_auth_required(self):
        trip = sample_trip(name="Trip1")
        res = self.client.patch(detail_url("trip", trip.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_method_auth_required(self):
        trip = sample_trip(name="Trip1")
        res = self.client.put(detail_url("trip", trip.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_method_auth_required(self):
        trip = sample_trip(name="Trip1")
        res = self.client.delete(detail_url("trip", trip.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
