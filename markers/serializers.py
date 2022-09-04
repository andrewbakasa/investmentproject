
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from rest_framework_gis.fields import GeometrySerializerMethodField
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis import serializers as gis_serializers
from .models import WorldBorder



from .models import  Marker
from store.models import Product

class MarkerSerializer(GeoFeatureModelSerializer):

	class Meta:
		model = Marker
		fields = '__all__'
		geo_field = 'location'

class ProductSerializer(GeoFeatureModelSerializer):
		
	#distance = serializers.CharField()
	#location_signature = serializers.PrimaryKeyRelatedField(read_only=True)
	location = GeometrySerializerMethodField(source='shop.location')
	#shop_name = serializers.StringRelatedField(read_only=True)
    
	def get_location(self, obj):
		return obj.shop.location
		
	class Meta:
		model = Product
		fields = ['name', 'image'] #shop_name
		geo_field = 'location'
		#read_only_fields = ['distance']

	# def to_representation(self, instance):
	# 	representation = super(ProductSerializer, self).to_representation(instance)
	# 	representation['location'] = instance.shop.location
	# 	representation['shopname'] = instance.shop.name
	# 	return representation

class WorldBorderSerializer(gis_serializers.GeoFeatureModelSerializer):
    """world border GeoJSON serializer."""

    class Meta:
        """World border serializer meta class."""

        fields = ("id", "name")
        geo_field = "mpoly"
        model = WorldBorder






