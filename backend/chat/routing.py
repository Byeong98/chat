from django.urls import re_path

from .consumers.chat_consumers import ChatConsumer
from .consumers.rooms_consumers import RoomsConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/chat/chatRooms/", RoomsConsumer.as_asgi()),
]