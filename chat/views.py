from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .serializers import MessageSerializer


class SendMessageAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            room_name = serializer.validated_data["room_name"]
            message = serializer.validated_data["message"]

            # WebSocket orqali xabarni yuborish
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"chat_{room_name}",
                {
                    "type": "chat_message",
                    "message": message
                }
            )

            return Response({"status": "success", "message": message}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
