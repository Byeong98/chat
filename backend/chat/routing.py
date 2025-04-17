from django.urls import re_path

from .consumers.chat_consumers import ChatConsumer
from .consumers.rooms_consumers import RoomsConsumer
from .consumers.chat_t import ChatTestConsumers

websocket_urlpatterns = [
    re_path(r"ws/chat/test/(?P<room_id>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_id>\w+)/$", ChatTestConsumers.as_asgi()),
    re_path(r"ws/chat/", RoomsConsumer.as_asgi()),
]