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
        self.room_group_name = f"chat_{self.room_name}"
        self.chat_room = await self.get_or_create_room(self.room_name,self.user)
        
        #현재 채널을 그룹에 추가 + 연결 수락
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    #현제 채널 그룹에서 제거
    async def disconnect(self, close_code):
        #사용자 삭제
        self.delete_user(self.room_name,self.user)
        users = self.get_room_users(self.room_name)
        if users:
            await self.delete_room(self.room_name)
        
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    #메시지 보내는 로직
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        image = text_data_json.get("image", None)
        
        #메시지 저장
        await self.create_message(room_name=self.chat_room,
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
    def get_or_create_room(self,room_name, user):
        room, created = ChatRoom.objects.get_or_create(name=room_name,)
        room.users.add(user)
        return room
    
    #해당채팅방에 있는 유저 확인하기
    @database_sync_to_async
    def get_room_users(self,room_name):
        room = ChatRoom.objects.get(name=room_name)
        users = room.users.all()
        return users
    
    #채팅방 삭제
    @database_sync_to_async
    def delete_room(self, room_name):
        ChatRoom.objects.filter(name=room_name).delete()
    
    #메시지를 데이터 베이스에 저장
    @database_sync_to_async
    def create_message(self, room_name, sender_user, message, image):
        Message.objects.create(
            chat_room=room_name,
            sender_user=sender_user,
            content=message,
            image=image,
        )
        

    #사용자 찾기
    @database_sync_to_async
    def get_user(self, username):
        user= User.objects.get(username=username)
        return user
    

    #채팅방 사용자 제거
    @database_sync_to_async
    def delete_user(self,room_name ,user):
        room = ChatRoom.objects.get(name=room_name)
        room.users.remove(user)