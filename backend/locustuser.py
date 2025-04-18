from locust import HttpUser, task, events
import random
from decouple import config


class ChatUserCreate(HttpUser):
    user_count = 0

    def on_start(self):
        # user_num = random.randint(1, 51)

        # 회원가입
        for user_num in range(1,101):
            signup = self.client.post(
                    "/api/accounts/signup/",
                    json={"email": f'{user_num}@test.com', "username": f"{user_num}", "password": "1234"}
                )
            
    
    @task
    def print_user(self):
        print(self.user_count)