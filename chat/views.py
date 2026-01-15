from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from drf_spectacular.utils import extend_schema

from .models import Message, ChatRoom, User
from .serializers import MessageSerializer, UserCreateSerializer, UserCreateResponseSerializer


@extend_schema(
    summary="Chat xonasidagi xabarlar ro'yxati",
    description="Ma'lum chat xonasidagi xabarlar ro'yxati",
    responses={
        200: MessageSerializer(many=True),
    },
)
class ChatMessagesList(generics.ListAPIView):
    """Ma'lum chat xonasidagi xabarlar ro'yxati"""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        room_name = self.kwargs["room_name"]
        user = self.request.user
        
        # Foydalanuvchi bu xonaga kirish huquqiga ega ekanligini tekshirish
        try:
            room = ChatRoom.objects.get(room_name=room_name)
            if room.user1 != user and room.user2 != user:
                raise PermissionDenied("Bu chat xonasiga kirish huquqingiz yo'q")
        except ChatRoom.DoesNotExist:
            raise NotFound(f"Chat xonasi topilmadi: {room_name}")
        
        return Message.objects.filter(room__room_name=room_name).order_by("timestamp")


@extend_schema(
    request=UserCreateSerializer,
    responses={
        201: UserCreateResponseSerializer,
        400: UserCreateSerializer,
    },
    summary="Yangi foydalanuvchi yaratish",
    description="Yangi foydalanuvchi yaratish va JWT tokenlar olish",
    tags=["Users"],
)
class UserCreateAPIView(APIView):
    serializer_class = UserCreateSerializer

    @extend_schema(
        request=UserCreateSerializer,
        responses={
            201: UserCreateResponseSerializer,
            400: UserCreateSerializer,
        },
    )
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
