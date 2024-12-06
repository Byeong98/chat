from config.celery import app

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .chat_redis import get_list_from_redis


#그룹에 보내는 메시지 비동기 처리
@app.task()
def send_room_list_celery(room_list_redis, room_list_db):
    channel_layer = get_channel_layer()

    #{chat_room_id : 접속자 수} 형식으로 변경 
    list_dict = { 
            name.decode('utf-8').split('.')[1]:length
            for name, length in room_list_redis
            }
    
    #Redis에 있는 사용자들 가져와서 입력
    list_rooms=[]
    for room in room_list_db:
                data ={
                    "name": room['name'],
                    "id":room['id'],
                    "users": list_dict.get(str(room['id']), 0),
                }
                list_rooms.append(data)

    #{chat_room_id : 접속자 수} 형식으로 변경 + 1~10위 가져오기
    rank_dict ={name.decode('utf-8').split('.')[1]:length
                        for name, length in room_list_redis[:10]}
    
    #딕셔너리 순서에 맞게 가져오기 (ZSET이라 랭킹 순서)
    rank_rooms=[]
    for k in rank_dict:
            for room in room_list_db:
                if room['id'] == int(k):
                    rank_rooms.append({
                        "name": room['name'],
                        "id":room['id'],
                        "users": rank_dict.get(str(room['id']))
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


