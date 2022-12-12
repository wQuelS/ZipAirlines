from django.db import models
from math import log


class Airplane(models.Model):
    id = models.IntegerField(primary_key=True)
    board_num = models.CharField(max_length=10, unique=True)
    passengers = models.IntegerField()
    fuel_tank = models.IntegerField(blank=True)
    consumption_per_minute = models.DecimalField(
        max_digits=7, decimal_places=5, blank=True
    )
    minutes_to_fly = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )

    @property
    def _get_tank_capacity(self) -> int:
        return self.id * 200

    @property
    def _get_consumption_per_minute(self) -> float:
        consumption_multiplier = 0.80
        passenger_consumption_rate = 0.002

        consumption = log(self.id) * consumption_multiplier

        if self.passengers >= 1:
            consumption += self.passengers * passenger_consumption_rate
        return round(consumption, 5)

    @property
    def _get_minutes_to_fly(self) -> float:
        minutes = self.fuel_tank / self.consumption_per_minute
        return round(minutes, 2)

    def save(self, *args, **kwargs) -> None:
        self.fuel_tank = self._get_tank_capacity
        self.consumption_per_minute = self._get_consumption_per_minute
        self.minutes_to_fly = self._get_minutes_to_fly
        super().save(*args, **kwargs)

    def __str__(self):
        return self.board_num
