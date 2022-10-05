
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
	distance = serializers.SerializerMethodField()
	rank = serializers.SerializerMethodField()
	uid = serializers.SerializerMethodField()
	username = serializers.SerializerMethodField()
	offer_symbol = serializers.SerializerMethodField()
	expected_symbol = serializers.SerializerMethodField()
	image = serializers.SerializerMethodField()
	#tag_source_username = serializers.SerializerMethodField() 
	#tag_target_username = serializers.SerializerMethodField() 
	source_id = serializers.SerializerMethodField()                                                                
	owner_id = serializers.SerializerMethodField() 

	
	tag_source_target = serializers.SerializerMethodField()
	matching_partner = serializers.SerializerMethodField()
	already_matched = serializers.SerializerMethodField()
	suitor = serializers.SerializerMethodField()
	def get_matching_partner(self, obj):
		try:
			return obj.get_matching_partner
		
		except:
			return 'NoData'

	def get_already_matched(self, obj):
		try:
			return obj.get_already_matched
		
		except:
			return 'NoData'

			
	def get_suitor(self, obj):
		try:
			return obj.get_suitor
		
		except:
			return 'NoData'
	def get_tag_source_target(self, obj):
		try:
			return obj.get_source_target
		
		except:
			return 'NoData'
	# def get_tag_target_username(self, obj):
	# 	try:
	# 		return obj.get_target
		
	# 	except:
	# 		return 'NoData'
	# def get_tag_source_username(self, obj):
	# 	try:
	# 		return obj.get_source
		
	# 	except:
	# 		return 'NoData'
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
	def get_rank(self, obj):
		try:
			#print(obj.distance)
			return obj.rank
		except:
			return None
	def get_location(self, obj):
		try:
			#print(obj.distance)
			return obj.residence.location
		except:
			return None
	def get_source_id(self, obj):
		try:
			#print(obj.distance)
			return obj.pk
		except:
			return None	
	def get_owner_id(self, obj):
		try:
			#print(obj.distance)
			return obj.pk
		except:
			return None	
	class Meta:
		model = TradedCurrency
		fields = ['uid', 'value', 'image', 'tag_source_target', 
				'owner_id', 'source_id','matching_partner','suitor', #'tag_target_username','tag_source_username',
				'rank', 'username', 'description', 'offer_symbol',  'expected_symbol',
				'rate_expected', 'distance', 'already_matched'] #
		geo_field = 'location'
		#read_only_fields = ['distance']

class ProductSerializer(GeoFeatureModelSerializer):
	location = GeometrySerializerMethodField(source='shop.location')
	distance = serializers.SerializerMethodField()
	pid = serializers.SerializerMethodField()
	shopname = serializers.SerializerMethodField()
	rank = serializers.SerializerMethodField()
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
	def get_rank(self, obj):
		try:
			#print(obj.distance)
			return obj.rank
		except:
			return None	
	class Meta:
		model = Product
		fields = ['pid', 'name', 'rank','image', 'price','distance', 'shopname'] 
		geo_field = 'location'
		#read_only_fields = ['distance']





