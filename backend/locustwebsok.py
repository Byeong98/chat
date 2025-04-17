from locust import HttpUser, task, events
import websocket
import time
import json
import random
from decouple import config

class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.ws = None

    def connect(self):
        self.ws = websocket.create_connection(self.url)

    def send(self, message):
        if self.ws:
            self.ws.send(json.dumps(message))

    def receive(self):
        if self.ws:
            return self.ws.recv()

    def close(self):
        if self.ws:
            self.ws.close()
            self.ws = None



class ChatUser(HttpUser):
    user_count = 0
    # users = [] # 생성한 사용자 id 값 저장
    # rooms =[] # 생성한 채팅방 id 값 저장

    # 테스트 시작될 때 실행
    def on_start(self):
        self.websocket_clients = {}


    # 테스트가 종료될 때 실행
    def on_stop(self):
        # 웹소켓 연결 종료
        for ws in self.websocket_clients.values():
            ws.close()

    # 테스트 한번 씩 실행하는 함수
    @task
    def print_user(self):
        user_num = random.randint(1, 51)
        room_num = random.choice([1,2,3])
        
        # 로그인 
        login = self.client.post(
                "/api/login/",
                json={"email": f'{user_num}@test.com', "password": "1234"}
            )
        token = login.json().get("access") # 웹소켓 접속을 위한 사용자 토큰값

        # 웹소켓 채팅방 입장
        if room_num not in self.websocket_clients:
            ws_client = WebSocketClient(f'ws://140.245.75.185:8000/ws/chat/' + f'{room_num}/?token={token}')
            ws_client.connect()
            self.websocket_clients[room_num] = ws_client
        else:
            ws_client = self.websocket_clients[room_num]


        self.user_count += 1
        print(self.user_count)