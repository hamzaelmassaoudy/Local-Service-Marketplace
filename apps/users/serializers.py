from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomerProfile, ProviderProfile

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        # 1. Create the User securely
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password) # Encrypts the password
        user.save()

        # 2. Create the specific profile based on Role
        if user.role == User.Role.PROVIDER:
            ProviderProfile.objects.create(user=user)
        else:
            # Default to customer
            CustomerProfile.objects.create(user=user)
            
        return user

class UserSerializer(serializers.ModelSerializer):
    """ Used to send user data back to frontend """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']