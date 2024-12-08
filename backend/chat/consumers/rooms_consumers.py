import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ..models import *
from ..chat_redis import get_list_from_redis
from ..tasks import send_room_list_celery



class RoomsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.home = "home"
        await self.channel_layer.group_add(self.home, self.channel_name)
        await self.accept()

        #홈화면 갱신
        send_room_list_celery.delay()


    #현제 채널 그룹에서 제거
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.home, self.channel_name)
        
