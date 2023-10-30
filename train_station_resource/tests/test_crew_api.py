from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from train_station_resource.serializers import (
    CrewSerializer
)
from .models_create_sample import sample_crew
from train_station_resource.models import Crew

CREW_URL = reverse("train_station:crew-list")


class UnauthenticatedCrewApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_method_auth_required(self):
        res = self.client.get(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_method_auth_required(self):
        res = self.client.post(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="Main@gmail.com", password="rvtquen"
        )
        self.client.force_authenticate(self.user)

    def test_list_crew(self):
        sample_crew()
        sample_crew()

        res = self.client.get(CREW_URL)

        crew_members = Crew.objects.all()
        serializers = CrewSerializer(crew_members, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializers.data)

    def test_create_crew_forbidden(self):
        res = self.client.post(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_crew_api_has_only_get_and_post_methods(self):
        res = self.client.post(CREW_URL)
        allowed_methods = res.headers["Allow"]
        forbidden_methods = ["PATCH", "PUT", "DELETE"]

        self.assertIn("GET", allowed_methods)
        self.assertIn("POST", allowed_methods)
        for method in forbidden_methods:
            self.assertNotIn(method, allowed_methods)


class AdminCrewApi(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email="test@gmai.com", password="rvtafj", is_staff=True
        )
        self.client.force_authenticate(self.admin)

    def test_admin_can_make_get_request(self):
        res = self.client.get(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_create_crew(self):

        crew_data = {
            "first_name": "Elon",
            "last_name": "Mask"
        }
        res = self.client.post(CREW_URL, crew_data)

        crew1 = Crew.objects.get(
            first_name=crew_data["first_name"],
            last_name=crew_data["last_name"]
        )  # Retrieve the specific instance
        serializer = CrewSerializer(crew1)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, serializer.data)
