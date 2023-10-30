import tempfile
import os

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from train_station_resource.serializers import (
    TrainSerializer,
    TrainListSerializer,
    TrainDetailSerializer,
)
from .models_create_sample import (
    sample_train_type,
    sample_train,
    sample_trip,
    detail_url
)
from train_station_resource.models import Train

TRAIN_URL = reverse("train_station:train-list")
TRIP_URL = reverse("train_station:trip-list")


def upload_train_image_url(train_id: int):
    return reverse("train_station:train-upload-image", args=[train_id])


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

    def test_upload_image_method_auth_required(self):
        train = sample_train(name="Train1")
        res = self.client.get(upload_train_image_url(train.id))
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

    def test_user_can_not_upload_image(self):
        train = sample_train(name="Train1")
        url = upload_train_image_url(train.id)

        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminTrainApi(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email="test@gmai.com", password="rvtafj"
        )
        self.client.force_authenticate(self.admin)

    def test_admin_can_make_get_request(self):
        res = self.client.get(TRAIN_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_train_can_get_detail(self):
        train = sample_train(name="Train1")
        res = self.client.get(detail_url("train", train.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_upload_image(self):
        train = sample_train(name="Train1")
        url = upload_train_image_url(train.id)

        res = self.client.post(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_admin_can_create_train(self):
        train_type = sample_train_type(name="TrainType1")

        train_data = {
            "name": "Train1",
            "cargo_num": 10,
            "seats_in_cargo": 20,
            "train_type": train_type.id
        }
        res = self.client.post(TRAIN_URL, train_data)

        train = Train.objects.get(
            name=train_data["name"]
        )  # Retrieve the specific instance
        serializer = TrainSerializer(train)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, serializer.data)


class TrainImageUploadTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email="test@gmai.com", password="rvtafj", is_staff=True
        )
        self.client.force_authenticate(self.admin)
        self.train = sample_train(name="MainTrain")

    def tearDown(self) -> None:
        self.train.image.delete()

    def test_upload_image_to_train(self):
        url = upload_train_image_url(self.train.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(
                url, {"image": ntf}, format="multipart"
            )
        self.train.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.train.image.path))

    def test_upload_image_bad_request(self):
        url = upload_train_image_url(self.train.id)
        res = self.client.post(
            url, {"image": "not image"}, format="multipart"
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_image_to_train_list_should_not_work(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)

            train_data = {
                "name": "Train1",
                "cargo_num": 10,
                "seats_in_cargo": 20,
                "train_type": sample_train_type(name="TrainType1").id,
                "image": ntf
            }
            res = self.client.post(
                TRAIN_URL, train_data, format="multipart"
            )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        train = Train.objects.get(name=train_data["name"])
        self.assertFalse(train.image)

    def test_image_url_is_shown_on_list(self):
        url = upload_train_image_url(self.train.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(
                url, {"image": ntf}, format="multipart"
            )
        res = self.client.get(TRAIN_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data["results"][0].keys())

    def test_image_url_is_shown_on_detail(self):
        url = upload_train_image_url(self.train.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(
                url, {"image": ntf}, format="multipart"
            )
        sample_trip(name="Trip1", train=self.train)
        res = self.client.get(TRIP_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("train_image", res.data["results"][0].keys())
