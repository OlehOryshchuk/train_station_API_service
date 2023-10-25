from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.db.models import Count, F

from rest_framework.test import APIClient
from rest_framework import status

from train_station_resource.serializers import (
    TripSerializer,
    TripListSerializer,
    TripDetailSerializer,
)
from .models_create_sample import (
    sample_trip,
    sample_train,
    sample_route,
    sample_station,
    sample_crew,
    detail_url,
)
from train_station_resource.models import Trip

TRIP_URL = reverse("train_station:trip-list")


def set_available_tickets_field():
    """Set available_tickets field in trip instances
    so we could compare data from trip view that has
    already calculated field available_tickets"""
    trips = Trip.objects.annotate(available_tickets=(
            F("train__cargo_num") * F("train__seats_in_cargo")
            - Count("tickets")
    ))
    return trips


def get_trip(trips, trip_id: Trip):
    """Get trip from trips queryset with available_ticket
    field"""
    return trips.get(id=trip_id)


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


class AuthenticatedTripApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="Main@gmail.com", password="rvtquen"
        )
        self.client.force_authenticate(self.user)

    def test_trip_list_has_available_tickets_field(self):
        sample_trip(name="Trip1")

        res = self.client.get(TRIP_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("available_tickets", res.data["results"][0])

    def test_trip_detail_has_taken_places_field(self):
        trip = sample_trip(name="Trip1")

        res = self.client.get(detail_url("trip", trip.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("taken_places", res.data)

    def test_list_trip(self):

        sample_trip(name="Trip1")
        sample_trip(name="Trip2")

        res = self.client.get(TRIP_URL)

        trips = set_available_tickets_field()
        serializers = TripListSerializer(trips, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializers.data)

    def test_trip_detail_page(self):
        trip = sample_trip(name="Trip1")

        res = self.client.get(detail_url("trip", trip.id))

        trip = Trip.objects.get(id=trip.id)
        serializers = TripDetailSerializer(trip)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializers.data)

    def test_filter_trip_list_by_train_id(self):
        train1 = sample_train(name="Train1")

        trip1 = sample_trip(name="Trip1")
        trip2 = sample_trip(name="Trip2")
        trip3 = sample_trip(name="Trip3")

        trip1.train = train1
        trip2.train = train1

        trip1.save()
        trip2.save()

        res = self.client.get(
            TRIP_URL, {"train": train1.id}
        )
        trips = set_available_tickets_field()
        serializer1 = TripListSerializer(get_trip(trips, trip1.id))
        serializer2 = TripListSerializer(get_trip(trips, trip2.id))
        serializer3 = TripListSerializer(get_trip(trips, trip3.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer3.data, res.data["results"])

    def test_filter_trip_list_by_route_source(self):
        route = sample_route(
            sample_station("Station1"),
            sample_station("Station2")
        )
        trip1 = sample_trip(name="Trip1")
        trip2 = sample_trip(name="Trip2")
        trip3 = sample_trip(name="Trip3")

        trip1.route = route
        trip2.route = route

        trip1.save()
        trip2.save()

        res = self.client.get(
            TRIP_URL, {"route__source": route.source.id}
        )

        trips = set_available_tickets_field()
        serializer1 = TripListSerializer(get_trip(trips, trip1.id))
        serializer2 = TripListSerializer(get_trip(trips, trip2.id))
        serializer3 = TripListSerializer(get_trip(trips, trip3.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer3.data, res.data["results"])

    def test_create_trip_forbidden(self):
        res = self.client.post(TRIP_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_train_api_has_only_get_and_post_methods(self):
        res = self.client.post(TRIP_URL)
        allowed_methods = res.headers["Allow"]
        forbidden_methods = ["PATCH", "PUT", "DELETE"]

        self.assertIn("GET", allowed_methods)
        self.assertIn("POST", allowed_methods)
        for method in forbidden_methods:
            self.assertNotIn(method, allowed_methods)


class AdminTripApi(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="test@gmai.com", password="rvtafj"
        )
        self.client.force_authenticate(self.admin)

    def test_admin_can_make_get_request(self):
        res = self.client.get(TRIP_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_trip_can_make_get_detail(self):
        trip = sample_trip(name="Trip1")
        res = self.client.get(detail_url("trip", trip.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_create_trip(self):
        route = sample_route(
            sample_station("Station1"),
            sample_station("Station2")
        )
        crew = sample_crew(
            first_name="Elon", last_name="Mask"
        )
        data = {
            "crew": [crew.id],
            "route": route.id,
            "train": sample_train("ChangedTrain").id,
            "departure_time": datetime.today(),
            "arrival_time": datetime.today() + timedelta(days=2),
        }

        res = self.client.post(TRIP_URL, data)

        trip = Trip.objects.get(
            train_id=data["train"]
        )  # Retrieve the specific instance
        serializer = TripSerializer(trip)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, serializer.data)

    def test_admin_trip_can_make_put_request(self):
        trip = sample_trip(name="Trip1")
        route = sample_route(
            sample_station("Station1"),
            sample_station("Station2")
        )
        crew = sample_crew(
            first_name="Elon", last_name="Mask"
        )
        data = {
            "crew": [crew.id],
            "route": route.id,
            "train": sample_train("ChangedTrain").id,
            "departure_time": datetime.today(),
            "arrival_time": datetime.today(),
        }

        res = self.client.put(
            detail_url("trip", trip.id),
            data
        )

        trip = Trip.objects.get(id=trip.id)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data["route"], trip.route.id,
        )
        self.assertEqual(
            res.data["crew"][0], crew.id,
        )
        self.assertEqual(
            res.data["train"], trip.train.id,
        )

    def test_admin_trip_can_make_patch_request(self):
        trip = sample_trip(name="Trip1")
        route = sample_route(
            sample_station("Station1"),
            sample_station("Station2")
        )
        data = {
            "crew": [],
            "route": route.id,
            "arrival_time": datetime.today() + timedelta(days=2),
        }

        res = self.client.patch(
            detail_url("trip", trip.id),
            data
        )
        trip = Trip.objects.get(id=trip.id)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data["crew"], []
        )
        self.assertEqual(
            res.data["route"], trip.route.id,
        )

    def test_admin_can_delete_trip(self):
        trip = sample_trip(name="Trip1")

        res = self.client.delete(
            detail_url("trip", trip.id)
        )

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Trip.DoesNotExist):
            Trip.objects.get(id=trip.id)
