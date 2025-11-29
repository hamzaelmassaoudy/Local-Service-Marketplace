import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from apps.bookings.models import Booking
from .serializers import ChatMessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.booking_id = self.scope['url_route']['kwargs']['booking_id']
        self.room_group_name = f'chat_{self.booking_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        # 1. Save to DB
        saved_message = await self.save_message(user, self.booking_id, message)
        
        # 2. Broadcast (Only if save was successful)
        if saved_message:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': saved_message
                }
            )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def save_message(self, user, booking_id, text):
        # Security: Ensure user is logged in
        if not user.is_authenticated:
            return None
            
        booking = Booking.objects.get(id=booking_id)
        
        # FIX: Use 'sender_id=user.pk' instead of 'user.id'
        # user.id is a UUID, but the database expects the Integer Primary Key (pkid)
        msg = ChatMessage.objects.create(sender_id=user.pk, booking=booking, text=text)
        
        # Return serialized data
        return ChatMessageSerializer(msg).data