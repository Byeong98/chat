from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import *
from decouple import config
import redis
from .chat_redis import get_users_from_redis
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
    
# class ConnectedUsersAPIView(APIView):
#     def get(self, request, room_id):
#         room = ChatRoom.objects.get(id=room_id)
#         users = [user.username for user in room.users.all()]
#         return Response({"users": users}, status=status.HTTP_200_OK)

