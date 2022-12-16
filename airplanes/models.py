from django.db import models

from django.core.validators import MinValueValidator
from rest_framework.exceptions import ValidationError


class Airline(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Airplane(models.Model):
    id = models.IntegerField(
        primary_key=True, validators=[MinValueValidator(1)]
    )
    capacity = models.IntegerField(validators=[MinValueValidator(1)])
    passengers = models.IntegerField()
    airline = models.ForeignKey(
        Airline, on_delete=models.CASCADE, related_name="airplanes", default=1
    )

    def clean(self) -> None:
        if self.passengers > self.capacity:
            raise ValidationError(
                "The number of passengers cannot be greater than the capacity of the airplane."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.airline.name} (id: {self.id}, capacity: {self.capacity}, passenger: {self.passengers})"
