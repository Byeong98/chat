from locust import HttpUser, task, between
import websocket
import time
import json
import random
from decouple import config
import redis

class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.ws = None

    def connect(self):
        start_time = time.time()
        self.ws = websocket.create_connection(self.url)
        end_time = time.time()
        self.connect_time = end_time - start_time # 웹소켓 접속시간 

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
    wait_time = between(1, 3)
    connection_times = []


    # 테스트 시작될 때 실행
    def on_start(self):
        self.websocket_clients = {}

        user_num = random.randint(1, 51)
        room_num = random.choice([3,4,5])

        # 로그인 
        login = self.client.post(
                "/api/login/",
                json={"email": f'{user_num}@test.com', "password": "1234"},
                headers={"Content-Type": "application/json"}
            )

        token = login.json().get("access") # 웹소켓 접속을 위한 사용자 토큰값

        # # 웹소켓 채팅방 입장
        if room_num not in self.websocket_clients:
            ws_client = WebSocketClient(f'ws://{config('ALLOWED_HOSTS')}:8000/ws/chat/' + f'{room_num}/?token={token}')
            ws_client.connect()
            self.connection_times.append(ws_client.connect_time)  # 연결 시간 저장
            self.websocket_clients[room_num] = ws_client
        else:
            ws_client = self.websocket_clients[room_num]

    # 정지시 평균 값
    def on_stop(self):
        avg = sum(self.connection_times) / len(self.connection_times)
        print(f"평균 접속 시간 : {avg:.4f}, 최대 접속 시간 : {max(self.connection_times):.4f}, 최소 접속 시간 : {min(self.connection_times):.4f}")

    # 테스트 한번 씩 실행하는 함수
    @task
    def print_user(self):
        pass

