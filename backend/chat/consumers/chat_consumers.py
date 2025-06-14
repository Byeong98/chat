import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ..models import *
import time
from ..chat_redis import *
from ..tasks import send_room_list_celery, remove_and_get_user
from rest_framework_simplejwt.tokens import AccessToken
import asyncio
from django.core.cache import cache

from asgiref.sync import sync_to_async
from django.db import connection

# 쿼리 초기화
@sync_to_async
def reset_queries():
    connection.queries_log.clear()
# 쿼리 수 찾기
@sync_to_async
def print_query_count():
    print(f"발생한 DB 쿼리 수: {len(connection.queries)}개")

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await reset_queries()
        start = time.perf_counter()

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.user = self.scope["user"]

        #같은 이름의 채팅방이 있는지 확인 및 생성
        self.chat_room = await self.get_or_create_room(self.room_id)
        self.room_group_name = f"chat_room_id.{self.chat_room['id']}"
        
        #Redis에 접속자 저장
        await add_user_to_redis(self.room_group_name, self.user.username)
        
        #현재 채널을 그룹에 추가 + 연결 수락
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        after_accept = time.perf_counter()
        print(f"채팅방 연결 완료: {after_accept - start:.4f} s")
        
        #채팅방 입장 전송
        save_messages = await self.get_message(self.chat_room['id'])
        users_redis = await get_users_from_redis(self.room_group_name)
        await self.channel_layer.group_send(
            self.room_group_name,{
                "type": "chat.update_users",  # 사용자 목록 갱신을 위한 이벤트
                "users": list(users_redis), # Redis에서 가져온 사용자 목록
                "message": f'{self.user.username}님이 입장 했습니다.', 
            }
        )

        after_group_send = time.perf_counter()
        print(f"접속자 리스트 접속 끝 : {after_group_send - after_accept:.4f} s")

        await self.send(text_data=json.dumps({
                    "save_messages":save_messages
                    }))
        
        end = time.perf_counter()
        print(f"총 걸린 시간: {end - start:.4f} s")
        await print_query_count()
        #홈화면 갱신
        send_room_list_celery.delay()

    #현제 채널 그룹에서 제거
    async def disconnect(self, close_code):
        
        # celery 비동기 실행
        remove_and_get_user.delay(self.room_group_name,
                                    self.user.username,
                                    self.chat_room['id']
                                    )

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    #메시지 보내는 로직
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        image = text_data_json.get("image", None)
        
        #이미지 파일이 있는 경우 미리 저장됨
        if image is not None:
            await self.create_message(chat_room=self.chat_room,
                                        sender_user=self.user,  
                                        message=message,    
                                        image=image)
        
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message",
                    "sender_user": self.user.id,
                    "sender_user_name": self.user.username,
                    "message": message, 
                    "image":image}
        )


    #메시지를 JSON으로 변환
    async def chat_message(self, event):
        message = event["message"]
        sender_user = event["sender_user"]
        image = event["image"]
        sender_user_name = event["sender_user_name"]
        
        await self.send(text_data=json.dumps({
                    "sender_user": sender_user,
                    "sender_user_name":sender_user_name,
                    "message": message, 
                    "image":image
                    }))
    

    #채팅방 접속자 디코딩 후 JSON으로 변환
    async def chat_update_users(self, event):
        users = event["users"]
        message = event["message"]
        users_str = [user.decode('utf-8') for user in users]
        await self.send(text_data=json.dumps({
                    "users": users_str,
                    "message": message,
                    }))


    #같은 이름의 채팅방을 가져오거난 생성
    @database_sync_to_async
    def get_or_create_room(self,room_id):
        cache_key = f"room:{room_id}"

        # Redis에서 먼저 확인
        cached_room = cache.get(cache_key)
        if cached_room:
            room_data = json.loads(cached_room)
            return room_data

        # DB 조회
        room = ChatRoom.objects.get(id=room_id)
        room_data = {
            "id": room.id,
            "name": room.name,
        }
        # Redis에 캐싱 
        cache.set(cache_key, json.dumps(room_data), timeout=60 * 60) 
        return room_data
    
    #해당채팅방에 있는 유저 확인하기
    @database_sync_to_async
    def get_room_users(self,room_id):
        room = ChatRoom.objects.get(id=room_id)
        return room.users.exists()
    
    #채팅방 삭제
    @database_sync_to_async
    def delete_room(self,room_id):
        room = ChatRoom.objects.get(id=room_id)
        room.delete()

    #사용자 찾기
    @database_sync_to_async
    def get_user(self, user_id):
        user= User.objects.get(id=user_id)
        return user

    #메시지를 데이터 베이스에 저장
    @database_sync_to_async
    def create_message(self, chat_room, sender_user, message, image):
        Message.objects.create(
            chat_room=chat_room,
            sender_user=sender_user,
            content=message,
            image=image,
        )
    
    #메시지 가져오기
    @database_sync_to_async
    def get_message(self, room_id):
        cache_key = f"room_mesage:{room_id}"

        # Redis에서 먼저 확인
        cached_room_masage = cache.get(cache_key)
        if cached_room_masage:
            room_masage = json.loads(cached_room_masage)
            return room_masage

        # DB에서 조회
        messages = Message.objects.filter(chat_room__id=room_id).order_by('add_date')

        dict_messages =[]
        for message in messages:
            dict_messages.append({
                "sender_user": message.sender_user.id,
                "sender_user_name": message.sender_user.username,
                "message": message.content, 
                "image": f"http://localhost:8000/media/{message.image}"
                })
            
        # Redis에 캐싱 
        cache.set(cache_key, json.dumps(dict_messages), timeout=60 * 60) 
        return dict_messages
