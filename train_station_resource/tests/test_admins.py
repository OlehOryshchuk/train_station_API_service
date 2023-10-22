from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models_create_sample import(
    sample_station,
)


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
