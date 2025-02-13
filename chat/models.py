from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, related_name="user1_chats", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="user2_chats", on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Chat: {self.user1.username} - {self.user2.username}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"
