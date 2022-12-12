from django.db import models
from math import log


class Company(models.Model):
    name = models.CharField(max_length=60)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "companies"

    def __str__(self):
        return self.name


class Airplane(models.Model):
    id = models.IntegerField(primary_key=True)
    board_num = models.CharField(max_length=10, unique=True)
    passengers = models.IntegerField()
    fuel_tank = models.IntegerField(blank=True)
    consumption_per_minute = models.DecimalField(
        max_digits=7, decimal_places=5, blank=True
    )

    @property
    def _get_tank_capacity(self) -> int:
        return self.id * 200

    @property
    def _get_consumption_per_minute(self) -> float:
        consumption = log(self.id) * 0.80

        if self.passengers >= 1:
            consumption *= self.passengers
        return round(consumption, 5)

    def save(self, *args, **kwargs) -> None:
        self.fuel_tank = self._get_tank_capacity
        self.consumption_per_minute = self._get_consumption_per_minute
        super().save(*args, **kwargs)

    def __str__(self):
        return self.board_num
