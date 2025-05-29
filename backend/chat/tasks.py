from config.celery import app

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import ChatRoom
from redis import Redis
from decouple import config
from .chat_redis import *



redis_client = Redis(host = config("REDIS_ADDRESS"),port= config("REDIS_PORT"),password=config("REDIS_PASSWORD"), db=0)

#그룹에 보내는 메시지 비동기 처리
@app.task()
def send_room_list_celery():
    channel_layer = get_channel_layer()

    #모든 채틷방 가져오기
    room_list_db = ChatRoom.objects.all()

    #Redis에서 모든 접속자 가져오기
    room_list_redis = redis_client.zrevrange('chatroom_ranking',0,-1, withscores=True)

    #{chat_room_id : 접속자 수} 형식으로 변경 
    list_dict = { 
            name.decode('utf-8').split('.')[1]:length
            for name, length in room_list_redis
            }
    
    #Redis에 있는 사용자들 가져와서 입력
    list_rooms=[]
    for room in room_list_db:
                list_rooms.append({
                    "name": room.name,
                    "id":room.id,
                    "users": list_dict.get(str(room.id), 0),
                })
                
    #{chat_room_id : 접속자 수} 형식으로 변경 + 1~10위 가져오기
    rank_dict ={name.decode('utf-8').split('.')[1]:length
                        for name, length in room_list_redis[:10]}

    #딕셔너리 순서에 맞게 가져오기 (ZSET이라 랭킹 순서)
    rank_rooms=[]
    for k in rank_dict:
        for room in room_list_db:
            if room.id == int(k):
                rank_rooms.append({
                    "name": room.name,
                    "id":room.id,
                    "users": rank_dict.get(str(room.id), 0)
                })

    #홈 랭킹, 리스트 갱신
    async_to_sync(channel_layer.group_send)(
        "home",
        {
            "type": "send_chatroom_list",
            "room_list": list_rooms,
            "room_rank": rank_rooms,
        }
    )

@app.task()
def remove_and_get_user(room_group_name,username,chat_room_id):
    channel_layer = get_channel_layer()

    #사용자 삭제
    users_count = async_to_sync(remove_user_to_redis)

    # 사용자가 없는 경우 채팅방 삭제
    if users_count:
        room = ChatRoom.objects.get(id=chat_room_id)
        room.delete()

    #퇴장 메시지 전송 + 접속자 리스트 갱신
    users_redis = async_to_sync(get_users_from_redis)(room_group_name)

    async_to_sync(channel_layer.group_send)(
        room_group_name,
        {
            "type": "chat.update_users",
            "users": list(users_redis),
            "message": f'{username}님이 퇴장 했습니다.'
        }
    )