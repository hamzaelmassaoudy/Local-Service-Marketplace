from rest_framework import serializers
from .models import Service, ServiceCategory
from apps.users.serializers import UserSerializer

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'slug', 'icon']

class ServiceSerializer(serializers.ModelSerializer):
    category_detail = ServiceCategorySerializer(source='category', read_only=True)
    category_id = serializers.UUIDField(write_only=True) 

    class Meta:
        model = Service
        fields = [
            'id', 'provider', 'title', 'description', 
            'price', 'is_hourly', 'location_lat', 'location_long',
            'category_id', 'category_detail', 'created_at'
        ]
        read_only_fields = ['provider', 'location_lat', 'location_long']

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_provider:
            raise serializers.ValidationError("Only providers can create services.")
            
        provider_profile = user.provider_profile
        validated_data['location_lat'] = provider_profile.latitude
        validated_data['location_long'] = provider_profile.longitude
        
        return Service.objects.create(provider=provider_profile, **validated_data)