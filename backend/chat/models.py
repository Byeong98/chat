from django.db import models

# Create your models here.


class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)    