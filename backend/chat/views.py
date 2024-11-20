from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *

# Create your views here.

class ChatRoomList(APIView):
    permission_classes=[AllowAny]

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

        return Response({"chat_rooms":data}, status=status.HTTP_200_OK)
    