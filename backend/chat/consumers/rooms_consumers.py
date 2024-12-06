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
        await self.chatroom_list()


    #현제 채널 그룹에서 제거
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.home, self.channel_name)
        


    #채탱방 리스트
    async def chatroom_list(self):
        #채팅방 마다 접속자 가져오기
        self.list_redis = await get_list_from_redis()

        self.room_list = await self.get_chat_room_list(self.list_redis)
        self.room_rank = await self.get_chat_room_rank(self.list_redis)

        await self.channel_layer.group_send(
            self.home, {"type": "send_chatroom_list",
                    "room_list" : self.room_list,
                    "room_rank" : self.room_rank,
                    })

    async def send_chatroom_list(self, event):
        room_list = event['room_list']
        room_rank = event['room_rank']

        await self.send(text_data=json.dumps({
            "room_list": room_list,
            "room_rank": room_rank,
        }))


    @database_sync_to_async
    def chat_room_list(self):
        chat_rooms = ChatRoom.objects.all()
        rooms=[]
        if chat_rooms.exists():
            for room in chat_rooms:
                data ={
                    "name": room.name,
                    "id":room.id,
                    "users": None,
                }
                rooms.append(data)
        return rooms

    @database_sync_to_async
    def get_chat_room_list(self, list_redis):
        chat_rooms = ChatRoom.objects.all()
        #{chat_room_id : 접속자 수} 형식으로 변경
        list_dict = { 
            name.decode('utf-8').split('.')[1]:length
            for name, length in list_redis
            }

        rooms=[]
        if chat_rooms.exists():
            for room in chat_rooms:
                data ={
                    "name": room.name,
                    "id":room.id,
                    "users": list_dict.get(str(room.id), 0),
                }
                rooms.append(data)
        return rooms
    

    @database_sync_to_async
    def get_chat_room_rank(self, rank_redis):
        #{chat_room_id : 접속자 수} 형식으로 변경 + 1~10위 가져오기
        rank_dict = {name.decode('utf-8').split('.')[1]:length
                        for name, length in rank_redis[:10] }
        #채팅방 아이디만 추출
        rank_redis_id = [int(name.decode('utf-8').split('.')[1]) for name, length in rank_redis]
        #채팅방 DB에서 조회
        chat_rooms = ChatRoom.objects.filter(id__in = rank_redis_id)
        
        rooms=[]
        for k in rank_dict:
            for room in chat_rooms:
                if room.id == int(k):
                    rooms.append({
                        "name": room.name,
                        "id":room.id,
                        "users": rank_dict.get(str(room.id))
                    })
        return rooms