from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from train_station_resource.models import (
    Station,
    Route,
    TrainType,
    Crew,
    Train,
    Trip,
    Order,
    Ticket,
)
from .models_create_sample import (
    sample_route,
    sample_station,
    sample_train_type,
    sample_train,
    sample_crew,
    sample_trip,
    sample_order,
)


class ModelsTest(TestCase):
    def test_station_string_representation(self):
        station = sample_station(name="Station1")
        self.assertEqual(str(station), station.name)

    def test_station_name_uniqueness(self):
        sample_station(name="Station1")
        with self.assertRaises(IntegrityError):
            sample_station(name="Station1")

    def test_route_string_rep_property(self):
        station1 = sample_station(name="Station1")
        station2 = sample_station(name="Station2")
        route1 = sample_route(station1, station2)

        expect_str = f"{station1} - {station2}"

        self.assertEqual(route1.string_repr, expect_str)

    def test_route_source_destination_are_not_same(self):
        station1 = sample_station(name="Station1")
        with self.assertRaises(ValidationError):
            sample_route(station1, station1)

    def test_route_source_destination_uniqueness(self):
        station1 = sample_station(name="Station1")
        station2 = sample_station(name="Station2")
        sample_route(station1, station2)

        with self.assertRaises(ValidationError):
            sample_route(station1, station2)

    def test_route_index_source(self):
        indexes = Route._meta.indexes
        self.assertEqual(indexes[0].fields[0], "source")

    def test_train_type_string_representation(self):
        train_type = sample_train_type(name="TrainType1")
        self.assertEqual(str(train_type), train_type.name)

    def test_train_type_name_uniqueness(self):
        sample_train_type(name="TrainType1")
        with self.assertRaises(IntegrityError):
            sample_train_type(name="TrainType1")

    def test_train_type_index_source(self):
        indexes = TrainType._meta.indexes
        self.assertEqual(indexes[0].fields[0], "name")

    def test_train_string_representation(self):
        train = sample_train_type(name="Train1")
        self.assertEqual(str(train), train.name)

    def test_train_name_uniqueness(self):
        sample_train(name="Train1")
        with self.assertRaises(IntegrityError):
            sample_train(name="Train1")

    def test_train_capacity_property(self):
        train = sample_train(
            name="Train1",
            cargo_num=10,
            seats_in_cargo=10,
        )

        self.assertEqual(train.capacity, 100)

    def test_crew_string_representation(self):
        crew_member = sample_crew(first_name="Joe", last_name="Biden")
        expect = f"{crew_member.first_name} {crew_member.last_name}"

        self.assertEqual(str(crew_member), expect)

    def test_crew_full_name_capacity(self):
        crew_member = sample_crew(first_name="Joe", last_name="Biden")
        expect = f"{crew_member.first_name} {crew_member.last_name}"

        self.assertEqual(crew_member.full_name, expect)

    def test_trip_string_representation(self):
        trip = sample_trip()
        expect = f"{trip.route} {trip.departure_time}"

        self.assertEqual(str(trip), expect)

    def test_trip_index_source(self):
        indexes = Trip._meta.indexes
        self.assertEqual(indexes[0].fields[0], "route")

    def test_order_string_representation(self):
        user = get_user_model().objects.create(
            email="main_user@gmail.com", password="Mainpassword123"
        )
        order = sample_order(user=user)

        self.assertEqual(str(order), f"{order.created_at}")

    def test_order_model_in_descending_order(self):
        user = get_user_model().objects.create(
            email="main_user@gmail.com", password="Mainpassword123"
        )
        order1 = sample_order(user=user)
        sample_order(user=user)
        order3 = sample_order(user=user)

        orders = Order.objects.all()

        self.assertEqual(orders.first(), order3)
        self.assertEqual(orders.last(), order1)
