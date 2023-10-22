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
    list_display = ["name", "longitude", "latitude"]


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    search_fields = ["source__name"]
    list_display = ["source", "destination", "distance"]


@admin.register(TrainType)
class TrainTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    search_fields = ["name", "train_type__name"]
    list_filter = ["cargo_num", "seats_in_cargo"]
    list_display = [
        "name",
        "cargo_num",
        "seats_in_cargo",
        "train_type"
    ]


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name"]


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    search_fields = ["route__source", "route__destination"]
    list_filter = ["train__train_type"]
    list_display = [
        "display_route_string_repr",
        "train",
        "departure_time",
        "arrival_time"
    ]

    def display_route_string_repr(self, obj):
        return obj.route.string_repr  # Reference the property

    display_route_string_repr.short_description = "Route"  # Customize the column header


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [TicketInline]
    search_fields = ["user__email"]
    list_display = [
        "user", "created_at"
    ]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    search_fields = ["order__user"]
    list_filter = ["trip"]
    list_display = [
        "trip",
        "order",
        "cargo",
        "seat",
    ]

    def display_route_string_repr(self, obj):
        return obj.route.string_repr  # Reference the property

    display_route_string_repr.short_description = "Route"  # Customize the column header
