from config.celery import app

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


#그룹에 보내는 메시지 비동기 처리
@app.task()
async def send_group_users_list_celery(room_group_name,users_redis, message):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        room_group_name,{
                "type": "chat.update_users",  # 사용자 목록 갱신을 위한 이벤트
                "users": list(users_redis), # Redis에서 가져온 사용자 목록
                "message": message,
            }
    )


