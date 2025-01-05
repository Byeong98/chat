from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from decouple import config
import redis
import json

rd = redis.StrictRedis(host = config("REDIS_ADDRESS"),port= config("REDIS_PORT"),password=config("REDIS_PASSWORD"), db=0)

class AccountsAPIView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        data = request.data
        username = data["username"]
        email = data["email"]
        password = data["password"]

        if not username or not email or not password:
            return Response(
                {"message": "모든 필드를 입력해 주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            User.objects.create_user(username, email, password)
            return Response({"message": "회원가입이 완료됐습니다.",
                        "username" : username},
                        status=status.HTTP_201_CREATED)
        except:
            return Response({"message": "닉네임 또는 이메일이 중복입니다."},
                            status=status.HTTP_400_BAD_REQUEST)
        

class LoginAPIView(TokenObtainPairView):
    def post(self, request,*args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data=response.data

        access_token = data.get('access')
        refresh_token = data.get('refresh')

        #쿠키에 저장
        response.set_cookie('access', str(access_token), 
                            max_age=3600,
                            httponly=True, 
                            samesite='Lax')
        response.set_cookie('refresh', str(refresh_token), 
                            max_age=3600,
                            httponly=True, 
                            samesite='Lax')
        
        return response

    