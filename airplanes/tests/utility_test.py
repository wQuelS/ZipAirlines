from math import log

from django.test import TestCase

from airplanes.airplane_utility import AirplaneUtility
from airplanes.models import Airplane, Airline


class AirplaneUtilityTest(TestCase):
    def setUp(self) -> None:
        self.airline = Airline.objects.create(name="TestAirline")
        self.airplane = Airplane.objects.create(
            id=7, airline=self.airline, capacity=100, passengers=50
        )
        self.airplane_utility = AirplaneUtility(self.airplane)

    def test_tank_capacity(self):
        self.assertEqual(self.airplane_utility.tank_capacity, 7 * 200)

    def test_consumption_per_minute(self):
        self.assertEqual(
            self.airplane_utility.consumption_per_minute,
            round((log(7) * 0.80) + (50 * 0.002), 2),
        )

    def test_minutes_to_fly(self):
        consumption = round((log(7) * 0.80) + (50 * 0.002), 2)
        self.assertEqual(
            self.airplane_utility.minutes_to_fly,
            round((7 * 200) / consumption, 2),
        )
