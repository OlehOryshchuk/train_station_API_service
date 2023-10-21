from django.test import TestCase
from django.db import IntegrityError

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


class ModelsTest(TestCase):
    def test_station_string_representation(self):
        station = sample_station(name="Station1")
        self.assertEqual(str(station), station.name)

    def test_station_name_uniqueness(self):
        sample_station(name="Station1")
        with self.assertRaises(IntegrityError):
            sample_station(name="Station1")

