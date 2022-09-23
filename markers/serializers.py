
from investments_appraisal.models import UserProfile
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from rest_framework_gis.fields import GeometrySerializerMethodField
from rest_framework_gis import serializers as gis_serializers
from .models import TradedCurrency



from .models import  Marker
from store.models import Product

class TradedCurrencySerializer(GeoFeatureModelSerializer):
	location = GeometrySerializerMethodField(source='residence.location')
	#shop_name = serializers.StringRelatedField(read_only=True)

	distance = serializers.SerializerMethodField()
	uid = serializers.SerializerMethodField()
	username = serializers.SerializerMethodField()
	offer_symbol = serializers.SerializerMethodField()
	expected_symbol = serializers.SerializerMethodField()
	image = serializers.SerializerMethodField()

	def get_image(self, obj):
		try:
			return UserProfile.objects.filter(user= obj.created_by).first().imageURL
		except:
			return None
	def get_expected_symbol(self, obj):
		try:
			return obj.currency_expected.symbol
		except:
			return None
	def get_offer_symbol(self, obj):
		try:
			return obj.currency_offered.symbol
		except:
			return None
	def get_uid(self, obj):
		try:
			return obj.pk
		except:
			return None
	def get_username(self, obj):
		try:
			return obj.created_by.username
		except:
			return None
	def get_distance(self, obj):
		try:
			#print(obj.distance)
			return obj.distance.m
		except:
			return None
	def get_location(self, obj):
		try:
			#print(obj.distance)
			return obj.residence.location
		except:
			return None
		
	class Meta:
		model = TradedCurrency
		fields = ['uid', 'value', 'image', 'username', 'description', 'offer_symbol',  'expected_symbol', 'rate_expected', 'distance'] 
		geo_field = 'location'
		#read_only_fields = ['distance']

class ProductSerializer(GeoFeatureModelSerializer):
	location = GeometrySerializerMethodField(source='shop.location')
	#shop_name = serializers.StringRelatedField(read_only=True)

	distance = serializers.SerializerMethodField()
	pid = serializers.SerializerMethodField()
	shopname = serializers.SerializerMethodField()
	def get_shopname(self, obj):
		try:
			return obj.shop.name
		except:
			return None
	def get_pid(self, obj):
		try:
			return obj.pk
		except:
			return None
	def get_distance(self, obj):
		try:
			#print(obj.distance)
			return obj.distance.m
		except:
			return None
	def get_location(self, obj):
		return obj.shop.location
		
	class Meta:
		model = Product
		fields = ['pid', 'name', 'image', 'price','distance', 'shopname'] 
		geo_field = 'location'
		#read_only_fields = ['distance']





