"""Markers admin."""

from django.contrib.gis import admin

from .models import Marker, TradedCurrency, UserLocation


@admin.register(Marker)
class MarkerAdmin(admin.OSMGeoAdmin):
    """Marker admin."""

    list_display = ("name", "location")

@admin.register(UserLocation)
class UserLocationAdmin(admin.OSMGeoAdmin):
    """Marker admin."""

    list_display = ("user", "location")

admin.site.register(TradedCurrency)
