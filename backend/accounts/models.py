from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    username = models.CharField("닉네임", max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    add_date = models.DateTimeField(auto_now_add=True)

    # USERNAME_FIELD를 이메일로 변경
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # 슈퍼유저 생성 시 필요한 필드

    def __str__(self):
        return self.email