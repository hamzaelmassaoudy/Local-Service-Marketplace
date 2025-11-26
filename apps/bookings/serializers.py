from rest_framework import serializers
from .models import Booking, Review
from apps.services.models import Service
from apps.services.serializers import ServiceSerializer

class BookingSerializer(serializers.ModelSerializer):
    service_detail = ServiceSerializer(source='service', read_only=True)
    service_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'customer', 'provider', 'service_id', 'service_detail',
            'status', 'scheduled_date', 'address', 
            'latitude', 'longitude', 'price', 'description', 'created_at'
        ]
        read_only_fields = ['customer', 'provider', 'price', 'status']

    def create(self, validated_data):
        service_id = validated_data.pop('service_id')
        service = Service.objects.get(id=service_id)
        customer = self.context['request'].user
        price = service.price 

        booking = Booking.objects.create(
            customer=customer,
            provider=service.provider.user,
            service=service,
            price=price,
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