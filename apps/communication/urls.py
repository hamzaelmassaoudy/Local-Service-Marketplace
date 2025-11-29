from django.urls import path
from .views import ChatHistoryView, SendMessageView

urlpatterns = [
    path('<uuid:booking_id>/messages/', ChatHistoryView.as_view(), name='chat-history'),
    path('<uuid:booking_id>/send/', SendMessageView.as_view(), name='chat-send'),
]