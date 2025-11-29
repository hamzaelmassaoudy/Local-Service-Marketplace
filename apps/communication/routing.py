from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Matches ws://localhost:8000/ws/chat/<uuid>/
    re_path(r'ws/chat/(?P<booking_id>[0-9a-f-]+)/$', consumers.ChatConsumer.as_asgi()),
]