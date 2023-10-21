from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from datetime import datetime

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


def sample_station(name: str) -> Station:
    return Station.objects.create(longitude=50, latitude=50, name=name)


def sample_route(source: Station, destination: Station) -> Route:
    return Route.objects.create(
        source=source, destination=destination, distance=100
    )


def sample_train_type(name: str) -> TrainType:
    return TrainType.objects.create(name=name)


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
