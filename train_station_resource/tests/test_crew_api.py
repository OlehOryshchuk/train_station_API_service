from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from train_station_resource.serializers import (
    RouteSerializer
)
from .models_create_sample import sample_crew
from train_station_resource.models import Crew

CREW_URL = reverse("train_station:crew-list")


class UnauthenticatedRouteApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_method_auth_required(self):
        res = self.client.get(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_method_auth_required(self):
        res = self.client.post(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)