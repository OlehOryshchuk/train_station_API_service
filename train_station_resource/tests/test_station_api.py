from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from train_station_resource.serializers import StationSerializer
from .models_create_sample import sample_station
from train_station_resource.models import Station

STATION_URL = reverse("train_station:station-list")


class UnauthenticatedStationApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(STATION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedStationApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="Main@gmail.com", password="rvtquen"
        )
        self.client.force_authenticate(self.user)

    def test_list_station(self):
        sample_station(name="Station1")
        sample_station(name="Station2")

        res = self.client.get(STATION_URL)

        stations = Station.objects.all()
        serializers = StationSerializer(stations, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializers.data)


