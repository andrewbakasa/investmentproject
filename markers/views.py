"""Markers view."""

from django.views.generic.base import TemplateView


import json

from django.core.serializers import serialize
from django.views.generic.base import TemplateView

from .models import Marker


class MarkersMapView(TemplateView):
    """Markers map view."""

    template_name = "markers/map.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["markers"] = json.loads(serialize("geojson", Marker.objects.all()))
        return context
