from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from decouple import config
import redis
import json

rd = redis.StrictRedis(host = config("REDIS_ADDRESS"),port= config("REDIS_PORT"),password=config("REDIS_PASSWORD"), db=0)

class ChatRoomList(APIView):
    # permission_classes=[AllowAny]

    def get(self, request):
        chat_rooms = ChatRoom.objects.all()

        rooms=[]
        for room in chat_rooms:
            data ={
                "name": room.name,
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
        for room in chat_rooms:
            data ={
                "name": room.name,
                "users": room.users.count(),
                "add_date" : room.add_date,
            }
            rooms.append(data)
        return Response({"chat_rooms":rooms}, status=status.HTTP_200_OK)


class ConnectedUsers(APIView):
    def get(self, request, roomname):
        room = ChatRoom.objects.get(name=f'chat_{roomname}')
        users = [user.username for user in room.users.all()]
        return  Response({"users":users}, status=status.HTTP_200_OK)