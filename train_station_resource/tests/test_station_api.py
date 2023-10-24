from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status

from train_station_resource.serializers import StationSerializer
from .models_create_sample import sample_station
from train_station_resource.models import Station
from train_station_resource.paginations import CustomPagination

STATION_URL = reverse("train_station:station-list")


class UnauthenticatedStationApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_method_auth_required(self):
        res = self.client.get(STATION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_method_auth_required(self):
        res = self.client.post(STATION_URL)
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

    def test_create_station_forbidden(self):
        res = self.client.post(STATION_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_station_api_has_only_get_and_post_methods(self):
        res = self.client.post(STATION_URL)
        allowed_methods = res.headers["Allow"]
        forbidden_methods = ["PATCH", "PUT", "DELETE"]

        self.assertIn("GET", allowed_methods)
        self.assertIn("POST", allowed_methods)
        for method in forbidden_methods:
            self.assertNotIn(method, allowed_methods)


class AdminStationApi(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email="test@gmai.com", password="rvtafj", is_staff=True
        )
        self.client.force_authenticate(self.admin)

    def test_admin_can_make_get_request(self):
        res = self.client.get(STATION_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_create_station(self):
        station_data = {
            "name": "Station1",
            "latitude": 50,
            "longitude": 50
        }
        res = self.client.post(STATION_URL, station_data)

        station1 = Station.objects.get(name=station_data["name"])  # Retrieve the specific instance
        serializer = StationSerializer(station1)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, serializer.data)

