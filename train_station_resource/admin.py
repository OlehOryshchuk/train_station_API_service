from django.contrib import admin

from .models import (
    Station,
    Route,
    Crew,
    Train,
    TrainType,
    Order,
    Ticket,
    Trip,
)


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    search_fields = ["name"]



