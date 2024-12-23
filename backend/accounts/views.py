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
    # permission_classes=[AllowAny]

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
        

# class Login_View(TokenObtainPairView):
#     def post(self, request,*args, **kwargs):
#         response = super().post(request, *args, **kwargs)
#         email = request.data.get('email')
#         user = User.objects.get(email=email)

#         data = f"{user.username}:{user.id}"
#         rd.sadd('current_users', json.dumps(data))

#         return response
    

# class get_logged_in_users(APIView):
#     permission_classes=[AllowAny]

#     def get(self, request):
#         users = rd.smembers('current_users')  # Set에서 모든 요소 가져오기
#         user_data = [json.loads(user) for user in users]
        
#         return Response({'count':len(user_data),'users': user_data})
    


#sesstion 기반 로그인
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.utils import timezone


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)

        login(request, user)
        
        return Response({'message': '로그인 완료','user':{'username':user.username, 'user_id':user.id}}, status=status.HTTP_200_OK)
    
class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': '로그아웃'}, status=status.HTTP_200_OK)

class get_logged_in_usersAPIView(APIView):
    # permission_classes=[AllowAny]
    def get(self, request):
        # 모든 활성 세션 가져오기
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        user_ids = []

        # 각 세션에서 사용자 ID 추출
        for session in sessions:
            data = session.get_decoded()
            user_id = data.get('_auth_user_id')
            if user_id:
                user_ids.append(user_id)

        # User 모델에서 사용자 정보 가져오기
        users = User.objects.filter(id__in=user_ids)
        user_data = [{"id": user.id, "username": user.username} for user in users]

        return Response({"user_count": len(user_data),"logged_in_users": user_data})