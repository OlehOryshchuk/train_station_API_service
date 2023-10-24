from datetime import datetime
from django.contrib.auth import get_user_model
from django.urls import reverse

from train_station_resource.models import (
    Station,
    Route,
    TrainType,
    Crew,
    Train,
    Trip,
    Order,
)


def sample_station(name: str, **param) -> Station:
    default = {
        "longitude": 50,
        "latitude": 50,
        "name": name,
    }
    default.update(**param)

    return Station.objects.create(**default)


def sample_route(source: Station, destination: Station) -> Route:
    return Route.objects.create(
        source=source, destination=destination, distance=100
    )


def sample_train_type(name: str) -> TrainType:
    return TrainType.objects.create(name=name)


def sample_train(name: str, **param) -> Train:
    default = {
        "name": name,
        "cargo_num": 5,
        "seats_in_cargo": 5,
        "train_type": sample_train_type(name=name),
        "image": None
    }

    default.update(**param)

    return Train.objects.create(**default)


def sample_crew(**param) -> Crew:
    default = {
        "first_name": "MainFirst",
        "last_name": "MainLast",
    }

    default.update(**param)

    return Crew.objects.create(**default)


def sample_trip(name: str, **param) -> Trip:
    station1 = sample_station(name=name)
    station2 = sample_station(name=name + name)

    default = {
        "route": sample_route(station1, station2),
        "train": sample_train(name=name),
        "departure_time": datetime.today(),
        "arrival_time": datetime.today()
    }

    default.update(**param)

    return Trip.objects.create(**default)


def sample_order(user: get_user_model(), **param) -> Order:
    default = {
        "user": user
    }

    default.update(**param)

    return Order.objects.create(**default)


def detail_url(view_name: str, instance_id: int):
    return reverse(f"train_station:{view_name}-detail", args=[instance_id])