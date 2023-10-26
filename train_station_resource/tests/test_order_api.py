import time

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from train_station_resource.serializers import (
    OrderListSerializer,
)
from .models_create_sample import (
    sample_trip,
    sample_order,
    sample_station,
    sample_route,
    sample_ticket,
    sample_train
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


class AuthenticatedOrderApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="Main@gmail.com", password="rvtquen"
        )

        self.client.force_authenticate(self.user)

    def test_orders_are_filtered_by_user(self):
        user2 = get_user_model().objects.create_user(
            email="Second@gmail.com", password="rvtquen2"
        )

        trip1 = sample_trip("MainTrip1")
        trip2 = sample_trip("MainTrip2")
        sample_ticket(user2, trip2)
        sample_ticket(user2, trip2, cargo=2)
        sample_ticket(self.user, trip1)
        sample_ticket(self.user, trip1, cargo=2)

        res = self.client.get(ORDER_URL)

        user_orders = Order.objects.filter(user=self.user)
        serializer = OrderListSerializer(user_orders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_list_order(self):
        sample_order(self.user)
        sample_order(self.user)

        res = self.client.get(ORDER_URL)

        orders = Order.objects.all()
        serializers = OrderListSerializer(orders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializers.data)

    def test_filter_order_list_by_tickets__trip__route(self):
        route = sample_route(
            sample_station("Station1"),
            sample_station("Station2")
        )
        trip1 = sample_trip(name="Trip1", route=route)
        trip2 = sample_trip(name="Trip2")
        ticket1 = sample_ticket(self.user, trip=trip1)
        ticket2 = sample_ticket(self.user, trip=trip1, cargo=2)
        ticket3 = sample_ticket(self.user, trip=trip2)

        res = self.client.get(
            ORDER_URL, {"tickets__trip__route": route.id}
        )

        serializer1 = OrderListSerializer(ticket1.order)
        serializer2 = OrderListSerializer(ticket2.order)
        serializer3 = OrderListSerializer(ticket3.order)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer3.data, res.data["results"])

    def test_ordering_order_list_in_ascending_order_by_created_at_field(self):
        sample_order(self.user)
        print("Sleep 2 sec")
        time.sleep(3)
        sample_order(self.user)

        res = self.client.get(
            ORDER_URL, {"ordering": "created_at"}
        )

        orders = Order.objects.all().order_by("created_at")
        serializer = OrderListSerializer(orders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data["results"], serializer.data
        )

    def test_user_can_create_valid_order(self):
        trip = sample_trip(name="TripForTicket")
        order_data = {
            "tickets": [
                {
                    "cargo": 1,
                    "seat": 1,
                    "trip": trip.id
                }
            ]
        }

        res = self.client.post(ORDER_URL, order_data, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_create_invalid_order_invalid_cargo_field(self):
        train = sample_train(
            name="Train1", seats_in_cargo=5, cargo_num=5
        )
        trip = sample_trip(name="TripForTicket", train=train)
        order_data = {
            "tickets": [
                {
                    "cargo": 6,
                    "seat": 5,
                    "trip": trip.id
                }
            ]
        }

        res = self.client.post(ORDER_URL, order_data, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_invalid_order_invalid_seat_field(self):
        train = sample_train(
            name="Train1", seats_in_cargo=5, cargo_num=5
        )
        trip = sample_trip(name="TripForTicket", train=train)
        order_data = {
            "tickets": [
                {
                    "cargo": 5,
                    "seat": 6,
                    "trip": trip.id
                }
            ]
        }

        res = self.client.post(ORDER_URL, order_data, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_not_create_order_without_tickets(self):
        order_data = {
            "tickets": []
        }

        res = self.client.post(ORDER_URL, order_data, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
