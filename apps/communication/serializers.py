from rest_framework import serializers
from .models import ChatMessage
from apps.users.serializers import UserSerializer

class ChatMessageSerializer(serializers.ModelSerializer):
    # This nests the full user object (Avatar, Name, etc.)
    sender_detail = UserSerializer(source='sender', read_only=True)
    
    # Custom fields for frontend logic
    is_me = serializers.SerializerMethodField()
    sender_role = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', 'booking', 'sender', 'sender_detail', 'text', 'created_at', 'is_read', 'is_me', 'sender_role']
        read_only_fields = ['booking', 'sender', 'created_at', 'is_read']

    def get_is_me(self, obj):
        # Returns True if the logged-in user sent this message (mostly for REST API calls)
        request = self.context.get('request')
        if request and request.user:
            return obj.sender == request.user
        return False

    def get_sender_role(self, obj):
        # Dynamically determine if sender is Provider or Customer for THIS booking
        if obj.sender == obj.booking.provider:
            return "Provider"
        elif obj.sender == obj.booking.customer:
            return "Customer"
        return "User"