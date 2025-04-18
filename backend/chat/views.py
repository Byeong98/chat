from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import *
from decouple import config
import redis

from django.contrib.auth import get_user_model


rd = redis.StrictRedis(host = config("REDIS_ADDRESS"),port= config("REDIS_PORT"),password=config("REDIS_PASSWORD"), db=0)

class ChatRoomCreateAPIView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        data = request.data
        room_name = data.get('roomName')

        try:
            room =  ChatRoom.objects.create(name=room_name)
            return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": '채팅방 이름이 중복 입니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 채팅방삭제 테스트
    def delete(self, request):
        data = request.data
        room_id = data.get('room_id')

        try:
            room =  ChatRoom.objects.get(id=room_id)
            room.delete()
            return Response({"message": "채팅방이 삭제되었습니다."}, status=204)
        except User.DoesNotExist:
            return Response({"error": "채팅방이 존재하지 않습니다."}, status=404)




class ChatRoomListAPIView(APIView):
    permission_classes=[AllowAny]

    def get(self, request):
        chat_rooms = ChatRoom.objects.prefetch_related('users').annotate(user_count=models.Count('users'))

        rooms=[]
        if chat_rooms.exists():
            for room in chat_rooms:
                data ={
                    "name": room.name,
                    "id":room.id,
                    "users": room.user_count,
                    "add_date" : room.add_date,
                }
                rooms.append(data)

        return Response({"chat_rooms":rooms}, status=status.HTTP_200_OK)

class ChatRoomRankAPIView(APIView):
    permission_classes=[AllowAny]

    def get(self, request):
        chat_rooms = ChatRoom.objects.prefetch_related('users').annotate(user_count=models.Count('users')).order_by('-user_count')
        
        rooms=[]
        if chat_rooms.exists():
            for room in chat_rooms:
                data ={
                    "name": room.name,
                    "id":room.id,
                    "users": room.users.count(),
                    "add_date" : room.add_date,
                }
                rooms.append(data)
        return Response({"chat_rooms":rooms}, status=status.HTTP_200_OK)


class MessageAPIView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        data = request.data

        room_id = data.get('room_id')
        user_id = data.get('user_id')
        image = request.FILES.get('image')
        
        room = get_object_or_404(ChatRoom, id=room_id )
        user = get_user_model().objects.get(id=user_id)
        
        message = Message.objects.create(
            chat_room=room,
            sender_user=user,
            image=image)
        
        image_url = request.build_absolute_uri(message.image.url)
        return Response({'image_url': image_url})

# class ConnectedUsersAPIView(APIView):
#     def get(self, request, room_id):
#         users_redis = rd.smembers(f"chat_room_id_{room_id}")
#         users = [user for user in users_redis]
#         return Response({"users": users}, status=status.HTTP_200_OK)
    
class ConnectedUsersAPIView(APIView):
    permission_classes=[AllowAny]

    def get(self, request, room_id):
        room = ChatRoom.objects.get(id=room_id)
        users = [user.username for user in room.users.all()]
        return Response({"users": users}, status=status.HTTP_200_OK)
    
    # 채팅방에 사용자 저장
    def post(self, request, room_id:int):
        users = User.objects.all() 
        room = ChatRoom.objects.get(id=room_id)
        for user in users:
            room.users.add(user)
        return Response({"room_id": room.id}, status=status.HTTP_200_OK)

from asgiref.sync import async_to_sync 
from .chat_redis import get_users_from_redis, add_user_to_redis
# redis 채팅방 사용자 조회 코드
class ConnectedUsersRedisAPIView(APIView):
    permission_classes=[AllowAny]

    def get(self, request, room_id):
        room_group_name = f"chat_room_id.{room_id}"
        users = async_to_sync(get_users_from_redis)(room_group_name)
        return Response({"users": list(users)}, status=status.HTTP_200_OK)
    
    def post(self, request, room_id):
        users = User.objects.all()
        room_group_name = f"chat_room_id.{room_id}"
        for user in users:
            async_to_sync(add_user_to_redis)(room_group_name, user.username)
        return Response({"users": room_group_name}, status=status.HTTP_200_OK)
