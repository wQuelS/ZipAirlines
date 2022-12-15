from decimal import Decimal
from math import log

from django.conf import settings

from airplanes.models import Airplane


class AirplaneUtility:
    """
    Class to perform calculations for Airplane fields
    """

    def __init__(self, airplane: Airplane):
        self.airplane = airplane

    @property
    def tank_capacity(self) -> int:
        return self.airplane.id * settings.BASE_TANK

    @property
    def consumption_per_minute(self) -> float:
        consumption = (
            log(self.airplane.id) * settings.CONSUMPTION_MULTIPLIER
        ) + (self.airplane.passengers * settings.PASSENGER_CONSUMPTION_RATE)
        return round(consumption, 2)

    @property
    def minutes_to_fly(self) -> float:
        minutes = self.tank_capacity / self.consumption_per_minute
        return round(minutes, 2)
