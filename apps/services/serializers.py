from rest_framework import serializers
from .models import Service, ServiceCategory
from apps.users.models import ProviderProfile

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'slug', 'icon']

class ProviderPublicSerializer(serializers.ModelSerializer):
    """Minimal info to show on the Service Card"""
    username = serializers.CharField(source='user.username')
    profile_image = serializers.ImageField(source='user.profile_image', read_only=True)

    class Meta:
        model = ProviderProfile
        # --- PHASE 9 UPDATE: Added working_start and working_end ---
        fields = [
            'business_name', 'rating', 'num_reviews', 'username', 
            'is_verified', 'city', 'profile_image',
            'working_start', 'working_end'
        ]

class ServiceSerializer(serializers.ModelSerializer):
    category_detail = ServiceCategorySerializer(source='category', read_only=True)
    provider_detail = ProviderPublicSerializer(source='provider', read_only=True)
    
    category_id = serializers.SlugRelatedField(
        queryset=ServiceCategory.objects.all(),
        slug_field='id', 
        source='category', 
        write_only=True
    )

    class Meta:
        model = Service
        fields = [
            'id', 'provider', 'provider_detail', 
            'title', 'description', 
            'price', 'is_hourly', 
            'location_lat', 'location_long', 'service_radius_km',
            'category_id', 'category_detail', 'created_at',
            'image'
        ]
        read_only_fields = ['provider']

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_provider:
            raise serializers.ValidationError("You must become a provider to post services.")
        
        # Fallback location if map not used
        if 'location_lat' not in validated_data:
            validated_data['location_lat'] = user.provider_profile.latitude
            validated_data['location_long'] = user.provider_profile.longitude
        
        return Service.objects.create(provider=user.provider_profile, **validated_data)