from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import *

# Create your views here.


class AccountsAPIView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        data = request.data
        username = data["username"]
        email = data["email"]
        password = data["password"]

        if not username or not email or not password:
            return Response(
                {"error": "모든 필드를 입력해 주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            User.objects.create_user(username, email, password)
            return Response({"message": "회원가입이 완료됬었습니다.",
                        "username" : username},
                        status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "닉네임 또는 이메일이 중복입니다."},
                            status=status.HTTP_400_BAD_REQUEST)