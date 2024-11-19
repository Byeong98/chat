from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class ChatRoomList(APIView):
    def get(self, request):
        """
        채팅방 리스트 받아오기 
        """
        return Response()
    
    def post(self, request):
        """
        채팅방 만들기 
        """
        return Response()
    

def ChatRoom(request):
    return render()