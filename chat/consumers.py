import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
from .models import ChatRoom, Message, User



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
        try:
            data = json.loads(text_data)
            sender_id = data.get("sender_id")
            message = data.get("message")

            if not sender_id or not message:
                await self.send(text_data=json.dumps({
                    "error": "sender_id va message majburiy"
                }))
                return

            sender = await self.get_user(sender_id)
            room = await self.get_room(self.room_name)

            msg = await self.create_message(room, sender, message)

            # Xonadagi hamma foydalanuvchilarga yuborish
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": msg["content"],
                    "sender": msg["sender"],
                    "timestamp": msg["timestamp"],
                    "message_id": msg["id"],
                }
            )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                "error": "Noto'g'ri JSON format"
            }))
        except ObjectDoesNotExist as e:
            await self.send(text_data=json.dumps({
                "error": f"Xatolik: {str(e)}"
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                "error": f"Server xatosi: {str(e)}"
            }))

    async def chat_message(self, event):
        """Xabarni JSON shaklda barcha foydalanuvchilarga yuborish"""
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_user(self, user_id):
        """Foydalanuvchini olish"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ObjectDoesNotExist(f"Foydalanuvchi topilmadi: {user_id}")

    @database_sync_to_async
    def get_room(self, room_name):
        """Chat xonasini olish"""
        try:
            return ChatRoom.objects.get(room_name=room_name)
        except ChatRoom.DoesNotExist:
            raise ObjectDoesNotExist(f"Chat xonasi topilmadi: {room_name}")

    @database_sync_to_async
    def create_message(self, room, sender, content):
        """Xabarni yaratish"""
        msg = Message.objects.create(room=room, sender=sender, content=content)
        return {
            "id": msg.id,
            "content": msg.content,
            "sender": sender.username,
            "timestamp": str(msg.timestamp),
        }
