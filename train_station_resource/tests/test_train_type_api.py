from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from train_station_resource.serializers import TrainTypeSerializer
from .models_create_sample import sample_train_type
from train_station_resource.models import TrainType

STATION_URL = reverse("train_station:traintype-list")


class UnauthenticatedTrainTypeApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_method_auth_required(self):
        res = self.client.get(STATION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_method_auth_required(self):
        res = self.client.post(STATION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTrainTypeApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="Main@gmail.com", password="rvtquen"
        )
        self.client.force_authenticate(self.user)

    def test_list_train_type(self):
        sample_train_type(name="TrainType1")
        sample_train_type(name="TrainType2")

        res = self.client.get(STATION_URL)

        stations = TrainType.objects.all()
        serializers = TrainTypeSerializer(stations, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializers.data)

    def test_create_train_type_forbidden(self):
        res = self.client.post(STATION_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_train_type_api_has_only_get_and_post_methods(self):
        res = self.client.post(STATION_URL)
        allowed_methods = res.headers["Allow"]
        forbidden_methods = ["PATCH", "PUT", "DELETE"]

        self.assertIn("GET", allowed_methods)
        self.assertIn("POST", allowed_methods)
        for method in forbidden_methods:
            self.assertNotIn(method, allowed_methods)

