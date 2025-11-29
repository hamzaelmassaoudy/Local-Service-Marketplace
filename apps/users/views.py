from rest_framework import generics, status, permissions, views, parsers
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404

from .models import User, ProviderProfile
from apps.bookings.models import Review
from apps.bookings.serializers import ReviewSerializer
from apps.services.models import Service
from apps.services.serializers import ServiceSerializer

from .serializers import (
    UserRegistrationSerializer, 
    CustomTokenObtainPairSerializer, 
    UserSerializer, 
    BecomeProviderSerializer,
    ProviderProfileSerializer,
    CustomerProfileSerializer
)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "message": "Account created successfully.",
        }, status=status.HTTP_201_CREATED)

class UserProfileView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        user = request.user
        data = request.data

        # 1. Update User Core fields (Avatar, Cover, Username)
        # Note: partial=True allows sending just one field
        user_serializer = UserSerializer(user, data=data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Update Provider Profile fields
        if hasattr(user, 'provider_profile'):
            provider_data = data.get('provider_profile')
            # Check if provider_data is a dict (JSON) or needs parsing (if sent as string in FormData)
            if provider_data and isinstance(provider_data, str):
                import json
                try: provider_data = json.loads(provider_data)
                except: pass
            
            if provider_data:
                ps = ProviderProfileSerializer(user.provider_profile, data=provider_data, partial=True)
                if ps.is_valid(): ps.save()

        # 3. Update Customer Profile fields
        if hasattr(user, 'customer_profile'):
            customer_data = data.get('customer_profile')
            if customer_data and isinstance(customer_data, str):
                import json
                try: customer_data = json.loads(customer_data)
                except: pass

            if customer_data:
                cs = CustomerProfileSerializer(user.customer_profile, data=customer_data, partial=True)
                if cs.is_valid(): cs.save()

        # Return fresh data
        return Response(UserSerializer(user).data)

class BecomeProviderView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BecomeProviderSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, 'provider_profile'):
            return Response({"message": "Already a provider"}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        ProviderProfile.objects.create(user=user, **serializer.validated_data)
        user.role = user.Role.PROVIDER
        user.save()
        
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

# --- NEW: UNIFIED PUBLIC PROFILE VIEW ---
class PublicUserProfileView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, username):
        target_user = get_object_or_404(User, username=username)
        
        # Base Data
        response_data = {
            "user": UserSerializer(target_user).data,
            "type": target_user.role
        }

        # 1. Provider Logic: Show Services & Reviews
        if target_user.role == User.Role.PROVIDER and hasattr(target_user, 'provider_profile'):
            # Fetch Services
            services = Service.objects.filter(provider__user=target_user, is_active=True)
            # Fetch Reviews
            reviews = Review.objects.filter(booking__provider=target_user).order_by('-created_at')
            
            response_data['services'] = ServiceSerializer(services, many=True).data
            response_data['reviews'] = ReviewSerializer(reviews, many=True).data
            
        # 2. Customer Logic
        elif target_user.role == User.Role.CUSTOMER:
            # We don't expose private booking details, just verified profile info.
            # In the future, we could add "Reviews written by this user" here.
            pass
        
        return Response(response_data)