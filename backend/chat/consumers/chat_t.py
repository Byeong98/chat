import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from ..models import *
import time
from ..chat_redis import *
from ..tasks import send_room_list_celery
from rest_framework_simplejwt.tokens import AccessToken


from rest_framework.test import APIClient
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

class ChatTestConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        await reset_queries()
        start = time.perf_counter()

        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.user = self.scope["user"]

        # 임시 데이터베이스 저장 ----------test
        self.chat_room = await self.get_or_create_room_and_user(self.room_id,self.user)
        self.room_group_name = f"chat_room_id.{self.chat_room.id}"
        
        #현재 채널을 그룹에 추가 + 연결 수락
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        after_accept = time.perf_counter()
        print(f"채팅방 연결 완료: {after_accept - start:.4f} s")
        
        #채팅방 입장 전송
        save_messages = await self.get_message(self.chat_room)


        users = await self.get_user_list(self.room_id)
        # 임시 입장 전송 ----------test
        await self.channel_layer.group_send(
            self.room_group_name,{
                "type": "chat.update_users",  # 사용자 목록 갱신을 위한 이벤트
                "users": users, 
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

    #현제 채널 그룹에서 제거
    async def disconnect(self, close_code):
        #사용자 삭제
        chat_room = await database_sync_to_async(ChatRoom.objects.get)(id=self.chat_room.id)

        # 유저 제거
        await database_sync_to_async(chat_room.users.remove)(self.user)

        # 유저 수 확인 후 방 삭제
        users_count = await database_sync_to_async(chat_room.users.count)()
        if users_count == 0:
            await self.delete_room(chat_room.id)
        
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    #메시지 보내는 로직
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        image = text_data_json.get("image", None)
        
        #이미지 파일이 있는 경우 미리 저장됨
        if not image:
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
        users_str = [user for user in users]
        await self.send(text_data=json.dumps({
                    "users": users_str,
                    "message": message,
                    }))


    #같은 이름의 채팅방을 가져오거난 생성
    @database_sync_to_async
    def get_or_create_room(self,room_id):
        # room, created = ChatRoom.objects.get_or_create(id=room_id)
        # return room
        room = ChatRoom.objects.get(id=room_id)
        return room
    
    # 데이터베이스 저장 ------- test 
    @database_sync_to_async
    def get_or_create_room_and_user(self,room_id, user):
        # room, created = ChatRoom.objects.get_or_create(id=room_id,name=f"room-{room_id}")
        # if room:
        #     room.users.add(user)
        # if created:
        #     print(created)
        # return room
        room = ChatRoom.objects.get(id=room_id)
        room.users.add(user)
        return room
    
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
    
    # 사용자 리스트 
    @database_sync_to_async
    def get_user_list(self, room_id):
        room = ChatRoom.objects.get(id=room_id)
        users = [user.username for user in room.users.all()]
        return users

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
    def get_message(self, room):
        messages = Message.objects.filter(chat_room=room).order_by('add_date')

        dict_messages =[]
        for message in messages:
            dict_messages.append({
                "sender_user": message.sender_user.id,
                "sender_user_name": message.sender_user.username,
                "message": message.content, 
                "image": f"http://localhost:8000/media/{message.image}"
                })
        return dict_messages
