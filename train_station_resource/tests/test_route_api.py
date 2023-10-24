from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from train_station_resource.serializers import (
    RouteSerializer,
    RouteListSerializer,
)
from .models_create_sample import sample_station, sample_route
from train_station_resource.models import Station, Route

ROUTE_URL = reverse("train_station:route-list")


class UnauthenticatedRouteApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_method_auth_required(self):
        res = self.client.get(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_method_auth_required(self):
        res = self.client.post(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="Main@gmail.com", password="rvtquen"
        )
        self.client.force_authenticate(self.user)

    def test_list_route(self):
        station1 = sample_station(name="Station1")
        station2 = sample_station(name="Station2")
        sample_route(station1, station2)
        sample_route(station2, station1)

        res = self.client.get(ROUTE_URL)

        routes = Route.objects.all()
        serializers = RouteListSerializer(routes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializers.data)

    def test_create_route_forbidden(self):
        res = self.client.post(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_route_api_has_only_get_and_post_methods(self):
        res = self.client.post(ROUTE_URL)
        allowed_methods = res.headers["Allow"]
        forbidden_methods = ["PATCH", "PUT", "DELETE"]

        self.assertIn("GET", allowed_methods)
        self.assertIn("POST", allowed_methods)
        for method in forbidden_methods:
            self.assertNotIn(method, allowed_methods)


class AdminRouteApi(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email="test@gmai.com", password="rvtafj", is_staff=True
        )
        self.client.force_authenticate(self.admin)

    def test_admin_can_make_get_request(self):
        res = self.client.get(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_create_route(self):
        station1 = sample_station(name="Station1")
        station2 = sample_station(name="Station2")

        route_data = {
            "source": station1.id,
            "destination": station2.id,
            "distance": 50
        }
        res = self.client.post(ROUTE_URL, route_data)

        route1 = Route.objects.get(
            destination=route_data["destination"],
            source=route_data["source"]
        )  # Retrieve the specific instance
        serializer = RouteSerializer(route1)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, serializer.data)
