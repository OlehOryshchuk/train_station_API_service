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


def sample_train(name: str, **param) -> Train:
    default = {
        "name": name,
        "cargo_num": 5,
        "seats_in_cargo": 5,
        "train_type": sample_train_type(name="MainTrainType"),
        "image": None
    }

    default.update(**param)

    return Train.objects.create(**default)


def sample_crew(**param) -> Train:
    default = {
        "first_name": "MainFirst",
        "last_name": "MainLast",
    }

    default.update(**param)

    return Crew.objects.create(**default)
