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
