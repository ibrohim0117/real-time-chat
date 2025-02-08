from rest_framework import serializers
from .models import Message, User

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "sender", "receiver", "message", "timestamp"]
        read_only_fields = ["id", "timestamp"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user