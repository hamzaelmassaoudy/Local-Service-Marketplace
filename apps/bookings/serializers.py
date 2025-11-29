from rest_framework import serializers
from math import radians, cos, sin, asin, sqrt
from .models import Booking, Review
from apps.services.models import Service
from apps.services.serializers import ServiceSerializer
from apps.users.serializers import UserSerializer 

def haversine(lon1, lat1, lon2, lat2):
    if lon1 is None or lat1 is None or lon2 is None or lat2 is None:
        return 0
    try:
        lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 
        return c * r
    except (ValueError, TypeError):
        return 0

class BookingSerializer(serializers.ModelSerializer):
    service_detail = ServiceSerializer(source='service', read_only=True)
    
    # --- NEW: Full User Details for Chat Context ---
    customer_detail = UserSerializer(source='customer', read_only=True)
    provider_detail = UserSerializer(source='provider', read_only=True)
    # -----------------------------------------------

    service_id = serializers.UUIDField(write_only=True)
    qr_code_data = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            'id', 'customer', 'customer_detail', 
            'provider', 'provider_detail', 
            'service_id', 'service_detail',
            'status', 'scheduled_date', 'address', 
            'latitude', 'longitude', 'distance_km', 
            'price', 'description', 'created_at',
            'qr_code_data'
        ]
        read_only_fields = ['customer', 'provider', 'price', 'status', 'distance_km', 'qr_code_data']

    def get_qr_code_data(self, obj):
        request = self.context.get('request')
        if request and request.user == obj.customer:
            return str(obj.verification_token)
        return None

    def validate(self, data):
        try:
            service = Service.objects.get(id=data['service_id'])
        except Service.DoesNotExist:
            raise serializers.ValidationError("Invalid Service ID")

        provider_profile = service.provider
        booking_time = data['scheduled_date'].time()
        
        if booking_time < provider_profile.working_start or booking_time > provider_profile.working_end:
            raise serializers.ValidationError(
                f"Provider is unavailable at this time. Working hours: {provider_profile.working_start} - {provider_profile.working_end}"
            )
        return data

    def create(self, validated_data):
        service_id = validated_data.pop('service_id')
        service = Service.objects.get(id=service_id)
        customer = self.context['request'].user
        price = service.price 

        book_lat = validated_data.get('latitude')
        book_lon = validated_data.get('longitude')
        service_lat = service.location_lat
        service_lon = service.location_long

        distance = haversine(service_lon, service_lat, book_lon, book_lat)

        booking = Booking.objects.create(
            customer=customer,
            provider=service.provider.user,
            service=service,
            price=price,
            distance_km=round(distance, 2),
            **validated_data
        )
        return booking

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'booking', 'rating', 'comment', 'created_at']
        read_only_fields = ['booking']

    def create(self, validated_data):
        booking_id = self.context['view'].kwargs['booking_id']
        booking = Booking.objects.get(id=booking_id)
        return Review.objects.create(booking=booking, **validated_data)