import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Foydalanuvchi ulanadi"""
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """Foydalanuvchi uzilganda xonadan chiqariladi"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Xabar qabul qilish va saqlash"""
        data = json.loads(text_data)
        sender_id = data["sender_id"]
        message = data["message"]

        sender = await self.get_user(sender_id)
        room = await self.get_room(self.room_name)

        msg = Message.objects.create(room=room, sender=sender, content=message)

        # Xonadagi hamma foydalanuvchilarga yuborish
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": msg.content,
                "sender": sender.username,
                "timestamp": str(msg.timestamp),
            }
        )

    async def chat_message(self, event):
        """Xabarni JSON shaklda barcha foydalanuvchilarga yuborish"""
        await self.send(text_data=json.dumps(event))

    @staticmethod
    async def get_user(user_id):
        """Foydalanuvchini olish"""
        return await User.objects.aget(id=user_id)

    @staticmethod
    async def get_room(room_name):
        """Chat xonasini olish yoki yaratish"""
        return await ChatRoom.objects.aget(room_name=room_name)
