from django.contrib.gis.db.models import PointField
from django.db import models


from django.contrib.gis import forms

from django.contrib.gis.db import models as geo_models
# class Parks(geo_models.Model):
#     park_name_en = geo_models.CharField(max_length=256)    
#     description = geo_models.TextField()
#     picture = geo_models.ImageField()
#     geom = geo_models.PointField(widget= forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}) )

@property
def picture_url(self):
    return self.picture.url

def __unicode__(self):
    return self.title
class Marker(models.Model):
    name = models.CharField(max_length=255)
    location = PointField(default=None)


from django.contrib.gis.db import models as gis_models

class WorldBorder(gis_models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = gis_models.CharField(max_length=50)
    area = gis_models.IntegerField()
    pop2005 = gis_models.IntegerField('Population 2005')
    fips = gis_models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = gis_models.CharField('2 Digit ISO', max_length=2)
    iso3 = gis_models.CharField('3 Digit ISO', max_length=3)
    un = gis_models.IntegerField('United Nations Code')
    region = gis_models.IntegerField('Region Code')
    subregion = gis_models.IntegerField('Sub-Region Code')
    lon = gis_models.FloatField()
    lat = gis_models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = gis_models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "World borders"

