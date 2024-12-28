from django.urls import re_path

from .consumers.chat_consumers import ChatConsumer
from .consumers.rooms_consumers import RoomsConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_id>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/chat/", RoomsConsumer.as_asgi()),
]