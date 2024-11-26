import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from decouple import config

rd = redis.StrictRedis(host = config("REDIS_ADDRESS"),port= config("REDIS_PORT"),password=config("REDIS_PASSWORD"), db=0)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.query_string = self.scope["query_string"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        username = str(self.query_string).split('=')[1][:-1]
        self.user =  await self.get_user(username)
        
        #같은 이름의 채팅방이 있는지 확인 및 생성
        self.chat_room = await self.get_or_create_room(self.room_name)
        self.room_group_name = f"chat_{self.chat_room.name}"
        
        #사용자 저장
        rd.sadd(f'{self.room_group_name}_users', json.dumps(self.user.username))

        #현재 채널을 그룹에 추가 + 연결 수락
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    #현제 채널 그룹에서 제거
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
        #사용자 삭제
        rd.srem(f'{self.room_group_name}_users', json.dumps(self.user.username))

    #메시지 보내는 로직
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        image = text_data_json.get("image", None)
        #메시지 저장
        
        add_message= await self.create_message(chat_room=self.chat_room,
                                                sender_user=self.user,  
                                                message=message,    
                                                image=image)
        
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message",
                    "sender_user": self.user.username,
                    "message": message, 
                    "image":image}
        )


    #메시지를 JSON으로 변환
    async def chat_message(self, event):
        message = event["message"]
        sender_user = event["sender_user"]
        image = event["image"]
        
        await self.send(text_data=json.dumps({
                    "sender_user": sender_user,
                    "message": message, 
                    "image":image
                    }))


    #같은 이름의 채팅방을 가져오거난 생성
    @database_sync_to_async
    def get_or_create_room(self, room_name):
        room, created = ChatRoom.objects.get_or_create(
            name=room_name 
        )
        return room


    
    #메시지를 데이터 베이스에 저장
    @database_sync_to_async
    def create_message(self, chat_room, sender_user, message, image):
        Message.objects.create(
            chat_room=chat_room,
            sender_user=sender_user,
            content=message,
            image=image,
        )
        
    #사용자 찾기
    @database_sync_to_async
    def get_user(self,username ):
        user= User.objects.get(username=username)
        return user