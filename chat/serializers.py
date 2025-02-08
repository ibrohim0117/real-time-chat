from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    room_name = serializers.CharField(max_length=100)
    message = serializers.CharField(max_length=500)
