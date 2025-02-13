from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Message, ChatRoom
from .serializers import MessageSerializer

class ChatMessagesList(generics.ListAPIView):
    """Ma'lum chat xonasidagi xabarlar ro‘yxati"""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_name = self.kwargs["room_name"]
        return Message.objects.filter(room__room_name=room_name).order_by("timestamp")
