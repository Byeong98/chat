from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_list_or_404, get_object_or_404
from .models import *
from decouple import config
import redis
import json

rd = redis.StrictRedis(host = config("REDIS_ADDRESS"),port= config("REDIS_PORT"),password=config("REDIS_PASSWORD"), db=0)

class ChatRoomCreate(APIView):
    def post(self, request):
        data = request.data
        room_name = data.get('roomName')

        try:
            room =  ChatRoom.objects.create(name=room_name)
            return Response({"room_id": room.id}, status=status.HTTP_201_CREATED)
        except:
            return Response({"message": '채팅방 이름이 중복 입니다.'}, status=status.HTTP_400_BAD_REQUEST)



class ChatRoomList(APIView):
    # permission_classes=[AllowAny]

    def get(self, request):
        chat_rooms = ChatRoom.objects.all()
        
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

class ChatRoomRank(APIView):
    # permission_classes=[AllowAny]

    def get(self, request):
        chat_rooms = ChatRoom.objects.annotate(user_count=models.Count('users')).order_by('-user_count')
        
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


class ConnectedUsers(APIView):
    def get(self, request, room_id):
        room = get_object_or_404(ChatRoom,id=room_id)
        users = []
        if room.users.exists():
            for user in room.users.all():
                users.append(user.username)
        return  Response({"users":users}, status=status.HTTP_200_OK)