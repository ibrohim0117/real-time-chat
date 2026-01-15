from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):

    def token(self):
        refresh = RefreshToken.for_user(self)
        data = {
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token)
        }
        return data


class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, related_name="user1_chats", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="user2_chats", on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['-id']

    def clean(self):
        """Validatsiya: user1 va user2 bir xil bo'lmasligi kerak"""
        if self.user1 == self.user2:
            raise ValidationError("user1 va user2 bir xil bo'lishi mumkin emas")
        
        # Bir xil foydalanuvchilar orasida faqat bir xona bo'lishi kerak
        # user1 va user2 o'rnini almashtirib ham tekshirish kerak
        if self.pk is None:  # Yangi xona yaratilayotganda
            existing_room = ChatRoom.objects.filter(
                (Q(user1=self.user1) & Q(user2=self.user2)) |
                (Q(user1=self.user2) & Q(user2=self.user1))
            ).first()
            if existing_room:
                raise ValidationError(
                    f"Bu foydalanuvchilar orasida allaqachon chat xonasi mavjud: {existing_room.room_name}"
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Chat: {self.user1.username} - {self.user2.username}"


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"
