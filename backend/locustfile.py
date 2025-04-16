from locust import HttpUser, task, events
import websocket
import time
import json
import random


class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.ws = None

    def connect(self):
        self.ws = websocket.create_connection(self.url)
    
    def send(self, message):
        self.ws.send(json.dumps(message))
    
    def receive(self):
        return self.ws.recv()
    
    def close(self):
        self.ws.close()


class ChatUser(HttpUser):
    user_count = 0
    users = [] # 생성한 사용자 id 값 저장
    rooms =[] # 생성한 채팅방 id 값 저장

    # 테스트 시작될 때 실행
    def on_start(self):
        self.Websocket_client = None # None으로 초기화하고 존재 여부 확인 후 close.
        # 채팅방 생성
        self.room_id_numbers = [] # 채팅방 id 갑 저장
        room_name = random.sample(range(1, 9999), 5)
        for i in room_name:
            response = self.client.post("/api/chat/", json={"roomName": f"{i}"})
            room_id = response.json().get('room_id')
            self.room_id_numbers.append(room_id)
            self.rooms.append(room_id) # 테스트 종료시 사용할 채팅방 리스트에 저장


    # 테스트가 종료될 때 실행
    def on_stop(self):
        if self.Websocket_client:
            self.Websocket_client.close()

        # 사용자 삭제
        for user_id in self.users:
            self.client.delete("/api/accounts/signup/",
                                json={"user_id":user_id})

        # 채팅방 삭제
        for room_id in self.rooms:
            self.client.delete("/api/chat/",
                                json={"room_id":room_id})

    # 테스트 한번 씩 실행하는 함수
    @task
    def print_user(self):
        user_num = random.randint(1, 9999)
        room_num = random.choice(self.room_id_numbers)

        # 회원가입
        signup = self.client.post(
                "/api/accounts/signup/",
                json={"email": f'{user_num}@test.com', "username": f"{user_num}", "password": "1234"}
            )
        self.users.append(signup.json().get('user_id')) # 테스트 종료시 삭제할 사용자 리스트에 저장
        
        # 로그인 
        login = self.client.post(
                "/api/login/",
                json={"email": f'{user_num}@test.com', "password": "1234"}
            )
        token = login.json().get("access") # 웹소켓 접속을 위한 사용자 토큰값

        # 웹소켓 채팅방 입장
        self.Websocket_client = WebSocketClient('ws://127.0.0.1:8000/ws/chat/' + f'{room_num}/?token={token}')
        self.Websocket_client.connect()

        # 채팅방 사용자 목록 갱신
        self.client.get(f"/api/{room_num}/users/")
        
        # 홈화면 채팅방 리스트 + 랭킹 갱신
        self.client.get("/api/chat/list")
        self.client.get("/api/chat/rank")

        self.user_count += 1
        print(self.user_count)