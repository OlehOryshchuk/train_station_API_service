from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from train_station_resource.serializers import (
    RouteSerializer,
    RouteListSerializer,
)
from .models_create_sample import (
    sample_train_type,
    sample_train,
    detail_url
)
from train_station_resource.models import Train

TRAIN_URL = reverse("train_station:train-list")


class UnauthenticatedTrainApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_get_method_auth_required(self):
        res = self.client.get(TRAIN_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_method_auth_required(self):
        res = self.client.post(TRAIN_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detail_method_auth_required(self):
        train1 = sample_train(name="Train1")
        res = self.client.get(detail_url("train", train1.id))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

