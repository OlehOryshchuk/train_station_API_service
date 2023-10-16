import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Station(models.Model):
    name = models.CharField(unique=True, max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self) -> str:
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="routes"
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="routes"
    )
    distance = models.PositiveIntegerField()

    class Meta:
        unique_together = ["source", "destination"]
        ordering = ["source", "destination"]

    def __str__(self) -> str:
        return f"{self.source}-{self.destination}"


class TrainType(models.Model):
    name = models.CharField(unique=True, max_length=150)

    def __str__(self) -> str:
        return self.name


class Train(models.Model):
    name = models.CharField(unique=True, max_length=255)
    cargo_num = models.PositiveIntegerField()
    places_in_cargo = models.PositiveIntegerField()
    train_type = models.ForeignKey(
        TrainType,
        related_name="trains",
        on_delete=models.CASCADE,
    )

    @property
    def capacity(self) -> int:
        return self.cargo_num * self.places_in_cargo

    def __str__(self) -> str:
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

    @property
    def full_name(self) -> str:
        return self.first_name + " " + self.last_name


class Trip(models.Model):
    route = models.ForeignKey(
        Route,
        related_name="trips",
        on_delete=models.CASCADE,
    )
    train = models.ForeignKey(
        Train,
        related_name="trips",
        on_delete=models.CASCADE,
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ["departure_time"]

    def __str__(self) -> str:
        return self.route + " " + self.departure_time
