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



