import random
import uuid
from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from airplanes.models import Airline, Airplane


AIRPLANES_URL = reverse("airplanes:airplane-list")
AIRLINE_URL = reverse("airplanes:airlines")


def sample_airline(**params):
    defaults = {"name": str(uuid.uuid4())}
    defaults.update(**params)

    return Airline.objects.create(**defaults)


def sample_airplane(**params):
    defaults = {
        "id": random.randint(1, 1000),
        "capacity": 50,
        "passengers": 15,
    }
    defaults.update(params)

    airline_params = params.get("airline") or {}
    defaults["airline"] = sample_airline(**airline_params)

    return Airplane.objects.create(**defaults)


class AirplaneApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_airplane_str(self):
        airplane = sample_airplane()

        self.assertEqual(
            str(airplane),
            f"{airplane.airline.name} "
            f"(id: {airplane.id}, capacity: {airplane.capacity}, passenger: {airplane.passengers})",
        )

    def test_maximum_10_planes(self):
        airline = sample_airline()

        for _ in range(1, 11):
            sample_airplane()

        data = {
            "id": 201,
            "airline": airline,
            "capacity": 50,
            "passengers": 15,
        }
        response = self.client.post(AIRPLANES_URL, data)

        self.assertEqual(Airplane.objects.count(), 10)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_less_than_10_planes(self):
        for _ in range(5):
            sample_airplane()

        data = {
            "id": 201,
            "airline": sample_airline(),
            "capacity": 50,
            "passengers": 15,
        }
        response = self.client.post(AIRPLANES_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_airplane_list(self):
        airline = sample_airline()

        for i in range(1, 4):
            Airplane.objects.create(
                id=i, airline=airline, capacity=40, passengers=12
            )

        response = self.client.get(AIRLINE_URL)

        airplanes = Airplane.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Airplane.objects.count(), 3)

    def test_fail_when_passengers_more_than_capacity(self):
        airline = sample_airline()

        data = {"id": 210, "airline": airline, "capacity": 50, "passenger": 51}
        instance = Airplane(
            id=201, airline=airline, capacity=50, passengers=60
        )

        response = self.client.post(AIRPLANES_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(ValidationError, instance.clean)

    def test_airplane_with_negative_data_input(self):
        airline = sample_airline()

        data = {"id": 225, "airline": airline, "capacity": 20, "passenger": -1}
        response = self.client.post(AIRPLANES_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
