from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from train_station_resource.serializers import (
    OrderSerializer,
    OrderListSerializer,
)
from .models_create_sample import (
    sample_trip,
    sample_order,
)
from train_station_resource.models import Order


ORDER_URL = reverse("train_station:order-list")


class UnauthenticatedOrderApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_method_auth_required(self):
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_method_auth_required(self):
        res = self.client.post(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
