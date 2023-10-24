from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from train_station_resource.serializers import (
    TrainSerializer,
    TrainListSerializer,
    TrainDetailSerializer,
    TrainImageSerializer,
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


class AuthenticatedTrainApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="Main@gmail.com", password="rvtquen"
        )
        self.client.force_authenticate(self.user)

    def test_list_train(self):
        sample_train(name="Train1")
        sample_train(name="Train2")

        res = self.client.get(TRAIN_URL)

        trains = Train.objects.all()
        serializers = TrainListSerializer(trains, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializers.data)

    def test_train_detail_page(self):
        train = sample_train(name="Train1")

        res = self.client.get(detail_url("train", train.id))

        train = Train.objects.get(id=train.id)
        serializers = TrainDetailSerializer(train)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializers.data)

    def test_filter_train_list_by_train_type(self):
        train_type1 = sample_train_type(name="TrainType1")

        train1 = sample_train(name="Train1")
        train2 = sample_train(name="Train2")
        train3 = sample_train(name="Train3")

        train1.train_type = train_type1
        train2.train_type = train_type1

        train1.save()
        train2.save()

        res = self.client.get(
            TRAIN_URL, {"train_type": train_type1.id}
        )

        serializer1 = TrainListSerializer(train1)
        serializer2 = TrainListSerializer(train2)
        serializer3 = TrainListSerializer(train3)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer3.data, res.data["results"])

    def test_train_list_search_by_train_name(self):
        train1 = sample_train(name="Train0")
        train2 = sample_train(name="Train0.5")
        train3 = sample_train(name="Train1")

        res = self.client.get(
            TRAIN_URL, {"search": train1.name}
        )

        serializer1 = TrainListSerializer(train1)
        serializer2 = TrainListSerializer(train2)
        serializer3 = TrainListSerializer(train3)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serializer1.data, res.data["results"])
        self.assertIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer3.data, res.data["results"])

    def test_create_train_forbidden(self):
        res = self.client.post(TRAIN_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_train_api_has_only_get_and_post_methods(self):
        res = self.client.post(TRAIN_URL)
        allowed_methods = res.headers["Allow"]
        forbidden_methods = ["PATCH", "PUT", "DELETE"]

        self.assertIn("GET", allowed_methods)
        self.assertIn("POST", allowed_methods)
        for method in forbidden_methods:
            self.assertNotIn(method, allowed_methods)
