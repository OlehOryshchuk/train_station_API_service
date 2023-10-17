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


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    search_fields = ["source", "destination"]
    list_filter = ["distance"]


@admin.register(TrainType)
class TrainTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
