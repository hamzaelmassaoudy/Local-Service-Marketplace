from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomerProfile, ProviderProfile

User = get_user_model()

# --- PROFILE SERIALIZERS ---

class ProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = ['business_name', 'bio', 'is_verified', 'rating', 'num_reviews', 'years_experience', 'latitude', 'longitude', 'city', 'working_start', 'working_end']
        read_only_fields = ['is_verified', 'rating', 'num_reviews']

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ['address', 'phone_number', 'latitude', 'longitude']

# --- USER SERIALIZERS ---

class UserSerializer(serializers.ModelSerializer):
    provider_profile = ProviderProfileSerializer(read_only=True)
    customer_profile = CustomerProfileSerializer(read_only=True)
    is_provider = serializers.SerializerMethodField()
    # Explicitly add image fields with use_url=True to ensure full absolute URLs
    profile_image = serializers.ImageField(required=False, use_url=True)
    cover_image = serializers.ImageField(required=False, use_url=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_provider', 'profile_image', 'cover_image', 'date_joined', 'provider_profile', 'customer_profile']
        read_only_fields = ['role', 'email', 'date_joined']

    def get_is_provider(self, obj):
        return hasattr(obj, 'provider_profile')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data, role=User.Role.CUSTOMER)
        user.set_password(password)
        user.save()
        CustomerProfile.objects.create(user=user)
        return user

class BecomeProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = ['business_name', 'bio', 'city']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data 
        return data