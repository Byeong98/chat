import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ..models import *
from decouple import config

rd = redis.StrictRedis(host = config("REDIS_ADDRESS"),port= config("REDIS_PORT"),password=config("REDIS_PASSWORD"), db=0)

class RoomsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.Home = "Home"
        await self.channel_layer.group_add(self.Home, self.channel_name)
        await self.accept()


    #현제 채널 그룹에서 제거
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.Home, self.channel_name)

    #메시지 보내는 로직
    async def receive(self, text_data):
        
        await self.channel_layer.group_send(
            self.Home.send(text_data=json.dumps({}))
        )


    async def chatroom_created(self, event):
        # 새 채팅방 정보를 클라이언트로 전송
        await self.send(text_data=json.dumps(event))
