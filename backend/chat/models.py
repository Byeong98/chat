from django.db import models
from accounts.models import *


# Create your models here.


class ChatRoom(models.Model):
    name = models.CharField(max_length=50,unique=True)
    users = models.ManyToManyField(User, related_name="chat_rooms")
    add_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    image = models.FileField(upload_to="chat_images/",blank=True, null=True)
    add_date = models.DateTimeField(auto_now_add=True)