from rest_framework import serializers
from .models import Message, User


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ["id", "sender", "content", "timestamp"]


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

