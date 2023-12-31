from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models_create_sample import (
    sample_station,
    sample_route,
    sample_train_type,
    sample_train,
    sample_crew,
    sample_trip,
    sample_order,
)
from train_station_resource.admin import TripAdmin, OrderAdmin


class AdminTest(TestCase):
    def setUp(self) -> None:
        self.admin = get_user_model().objects.create_superuser(
            email="admin@gmail.com", password="rvtwfafhg"
        )
        self.client.force_login(self.admin)

    def test_admin_station_site_has_require_fields(self):
        station = sample_station(name="Station1")
        url = reverse(
            "admin:train_station_resource_station_changelist"
        )
        res = self.client.get(url)

        self.assertContains(res, station.name)
        self.assertContains(res, station.longitude),
        self.assertContains(res, station.latitude),

    def test_admin_station_search_by_name(self):
        station1 = sample_station(name="MainStation")
        station2 = sample_station(name="SecondStation")

        url = reverse(
            "admin:train_station_resource_station_changelist"
        )

        res = self.client.get(url, {"q": station1.name.lower()})

        changelist = res.context["cl"]
        self.assertIn(
            station1, changelist.queryset
        )
        self.assertNotIn(
            station2, changelist.queryset
        )

    def test_admin_route_site_has_require_fields(self):
        station1 = sample_station(name="Station1")
        station2 = sample_station(name="Station2")
        route1 = sample_route(station1, station2)

        url = reverse(
            "admin:train_station_resource_route_changelist"
        )
        res = self.client.get(url)

        self.assertContains(res, route1.source)
        self.assertContains(res, route1.destination),
        self.assertContains(res, route1.distance),

    def test_admin_route_search_by_source(self):
        station1 = sample_station(name="MainStation")
        station2 = sample_station(name="SecondStation")
        route1 = sample_route(station1, station2)
        route2 = sample_route(station2, station1)

        url = reverse(
            "admin:train_station_resource_route_changelist"
        )

        res = self.client.get(url, {"q": station1.name.lower()})

        changelist = res.context["cl"]
        self.assertIn(
            route1, changelist.queryset
        )
        self.assertNotIn(
            route2, changelist.queryset
        )

    def test_trip_type_admin_has_require_field(self):
        train_type = sample_train_type(name="TrainType1")

        url = reverse(
            "admin:train_station_resource_traintype_changelist"
        )

        res = self.client.get(url)

        self.assertContains(res, str(train_type))

    def test_admin_train_type_search_by_name(self):
        train_type1 = sample_train_type(name="TrainType1")
        train_type2 = sample_train_type(name="TrainType2")

        url = reverse(
            "admin:train_station_resource_traintype_changelist"
        )

        res = self.client.get(url, {"q": train_type1.name.lower()})

        changelist = res.context["cl"]
        self.assertIn(train_type1, changelist.queryset)
        self.assertNotIn(train_type2, changelist.queryset)

    def test_train_admin_has_require_field(self):
        train = sample_train(name="Train1")

        url = reverse(
            "admin:train_station_resource_train_changelist"
        )

        res = self.client.get(url)

        self.assertContains(res, train.name)
        self.assertContains(res, train.cargo_num)
        self.assertContains(res, train.seats_in_cargo)
        self.assertContains(res, train.train_type)

    def test_admin_train_search_by_name(self):
        train1 = sample_train(name="Train1")
        train2 = sample_train(name="Train2")

        url = reverse(
            "admin:train_station_resource_train_changelist"
        )

        res = self.client.get(url, {"q": train1.name.lower()})

        changelist = res.context["cl"]
        self.assertIn(train1, changelist.queryset)
        self.assertNotIn(train2, changelist.queryset)

    def test_admin_train_search_by_train_type_name(self):
        train_type1 = sample_train_type(name="TrainType1")
        train_type2 = sample_train_type(name="TrainType2")
        train1 = sample_train(name="Train1", train_type=train_type1)
        train2 = sample_train(name="Train2", train_type=train_type2)

        url = reverse(
            "admin:train_station_resource_train_changelist"
        )

        res = self.client.get(url, {"q": train_type1.name.lower()})

        changelist = res.context["cl"]
        self.assertIn(train1, changelist.queryset)
        self.assertNotIn(train2, changelist.queryset)

    def test_admin_train_filter_by_cargo_num(self):
        train1 = sample_train(name="Train1", cargo_num=10)
        train2 = sample_train(name="Train2", cargo_num=15)

        url = reverse(
            "admin:train_station_resource_train_changelist"
        )

        res = self.client.get(url, {"cargo_num": train1.cargo_num})

        changelist = res.context["cl"]
        self.assertIn(train1, changelist.queryset)
        self.assertNotIn(train2, changelist.queryset)

    def test_admin_train_filter_by_seats_in_cargo(self):
        train1 = sample_train(name="Train1", seats_in_cargo=10)
        train2 = sample_train(name="Train2", seats_in_cargo=15)

        url = reverse(
            "admin:train_station_resource_train_changelist"
        )

        res = self.client.get(url, {"seats_in_cargo": train1.seats_in_cargo})

        changelist = res.context["cl"]
        self.assertIn(train1, changelist.queryset)
        self.assertNotIn(train2, changelist.queryset)

    def test_crew_admin_has_require_field(self):
        crew_member = sample_crew(
            first_name="Mike", last_name="Tyson"
        )

        url = reverse(
            "admin:train_station_resource_crew_changelist"
        )

        res = self.client.get(url)

        self.assertContains(res, str(crew_member))

    def test_admin_crew_search_by_first_name_and_last_name(self):
        crew_member1 = sample_crew(
            first_name="First1", last_name="Last1"
        )
        crew_member2 = sample_crew(
            first_name="First2", last_name="Last2"
        )

        url = reverse(
            "admin:train_station_resource_crew_changelist"
        )

        res1 = self.client.get(
            url, {"q": crew_member1.first_name.lower()}
        )
        res2 = self.client.get(
            url, {"q": crew_member1.last_name.lower()}
        )

        changelist1 = res1.context["cl"]
        self.assertIn(crew_member1, changelist1.queryset)
        self.assertNotIn(crew_member2, changelist1.queryset)

        changelist2 = res2.context["cl"]
        self.assertIn(crew_member1, changelist2.queryset)
        self.assertNotIn(crew_member2, changelist2.queryset)

    def test_trip_admin_has_require_field(self):
        trip = sample_trip(name="Trip1")

        url = reverse(
            "admin:train_station_resource_trip_changelist"
        )

        res = self.client.get(url)

        self.assertContains(res, trip.route.string_repr)
        self.assertContains(res, trip.train)
        self.assertIn("departure_time", TripAdmin.list_display)
        self.assertIn("arrival_time", TripAdmin.list_display)

    def test_admin_trip_search_by_route_source_name(self):
        trip1 = sample_trip(name="Trip1")
        trip2 = sample_trip(name="Trip2")

        url = reverse(
            "admin:train_station_resource_trip_changelist"
        )

        res = self.client.get(
            url, {"q": trip1.route.source.name.lower()}
        )

        changelist = res.context["cl"]
        self.assertIn(trip1, changelist.queryset)
        self.assertNotIn(trip2, changelist.queryset)

    def test_admin_trip_filter_by_train_type_id(self):
        train_type = sample_train_type(name="TrainType1")
        trip1 = sample_trip(name="Trip1")
        trip2 = sample_trip(name="Trip2")
        trip1.train.train_type = train_type
        trip1.train.save()

        url = reverse(
            "admin:train_station_resource_trip_changelist"
        )

        res = self.client.get(
            url, {"train__train_type__id__exact": train_type.id}
        )

        changelist = res.context["cl"]

        self.assertIn(trip1, changelist.queryset)
        self.assertNotIn(trip2, changelist.queryset)

    def test_order_admin_has_require_field(self):
        user = get_user_model().objects.create(
            email="user@gmail.com", password="rvrtgga"
        )
        order = sample_order(user=user)

        url = reverse(
            "admin:train_station_resource_order_changelist"
        )

        res = self.client.get(url)

        self.assertContains(res, order.user.email)
        self.assertIn("created_at", OrderAdmin.list_display)

    def test_order_admin_search_by_user_email(self):
        user1 = get_user_model().objects.create(
            email="user1@gmail.com", password="rvrtgga1"
        )
        user2 = get_user_model().objects.create(
            email="user2@gmail.com", password="rvrtgga2"
        )
        order1 = sample_order(user=user1)
        order2 = sample_order(user=user2)

        url = reverse(
            "admin:train_station_resource_order_changelist"
        )

        res = self.client.get(url, {"q": user1.email})

        changelist = res.context["cl"]
        self.assertIn(order1, changelist.queryset)
        self.assertNotIn(order2, changelist.queryset)
