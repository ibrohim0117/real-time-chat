from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserCreateSerializer

from .models import Message, ChatRoom, User
from .serializers import MessageSerializer

class ChatMessagesList(generics.ListAPIView):
    """Ma'lum chat xonasidagi xabarlar ro‘yxati"""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_name = self.kwargs["room_name"]
        return Message.objects.filter(room__room_name=room_name).order_by("timestamp")



class UserCreateAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                "username": user.username,
                'access_token': user.token()['access_token'],
                'refresh_token': user.token()['refresh_token'],
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
