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
        related_name="source_routes"
    )
    destination = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        related_name="destination_routes"
    )
    distance = models.PositiveIntegerField()

    class Meta:
        unique_together = ["source", "destination"]
        ordering = ["source", "destination"]
        indexes = [
            models.Index(fields=["source"])
        ]

    @property
    def string_repr(self) -> str:
        return f"{self.source} - {self.destination}"


class TrainType(models.Model):
    name = models.CharField(unique=True, max_length=150)
    description = models.TextField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"])
        ]

    def __str__(self) -> str:
        return self.name


def train_image_file_path(instance: "Train", filename) -> str:
    """Return filename in format 'train_name_uuid4.extension'
        and store it in MEDIA_URL/uploads/trains/train_name_uuid4.extension
    """

    _, extension = os.path.split(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads", "trains", filename)


class Train(models.Model):
    name = models.CharField(unique=True, max_length=255)
    cargo_num = models.PositiveIntegerField()
    seats_in_cargo = models.PositiveIntegerField()
    train_type = models.ForeignKey(
        TrainType,
        related_name="trains",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=train_image_file_path,
    )

    @property
    def capacity(self) -> int:
        return self.cargo_num * self.seats_in_cargo

    def __str__(self) -> str:
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Crew member"
        verbose_name_plural = "Crew members"

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name

    @property
    def full_name(self) -> str:
        return self.first_name + " " + self.last_name


class Trip(models.Model):
    crew = models.ManyToManyField(Crew)
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
        indexes = [
            models.Index(fields=["route"])
        ]

    def __str__(self) -> str:
        return f"{self.route} {self.departure_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    cargo = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
    )

    @staticmethod
    def validate_ticket(
            cargo: int,
            seat: int,
            train: Train,
            error_to_raise
    ):
        for ticket_attr_value, ticket_attr_name, train_attr_name in [
            (cargo, "cargo", "cargo_num"),
            (seat, "seat", "seats_in_cargo")
        ]:
            train_attr_value = getattr(train, train_attr_name)

            if not (1 <= ticket_attr_value <= train_attr_value):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        "number must be in available range: "
                        f"(1, {train_attr_value})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.cargo,
            self.seat,
            self.trip.train,
            ValidationError,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()

        return super().save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self) -> str:
        return (
            f"{str(self.trip)} (cargo: {self.cargo}, seat: {self.seat})"
        )

    class Meta:
        unique_together = ["cargo", "seat", "trip"]
        ordering = ["cargo", "seat"]
