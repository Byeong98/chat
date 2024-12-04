from locust import User, task, events
import websocket
import time
import json


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


class ChatUser(User):
    # 기본 호스트 URL 설정 (WebSocket 서버 주소)
    
    def on_start(self):
        """테스트가 시작될 때 실행"""
        self.client = WebSocketClient('ws://127.0.0.1:8000/ws/chat/' + '6' + '/' + '?user=123')
        self.client.connect()
    
    def on_stop(self):
        """테스트가 종료될 때 실행"""
        self.client.close()
    
    @task
    def send_message(self):
        """메시지 전송 작업"""
        message = {
            "message": "Hello, this is a test message!",
            "image": None
        }
        self.client.send(message)
        response = self.client.receive()
        time.sleep(20)
        print(response)
        
