from rest_framework import serializers
from .models import Message, ActiveUser


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    """
    class Meta:
        model = Message
        fields = ['id', 'username', 'message_text', 'timestamp']
        read_only_fields = ['id', 'timestamp']

    def validate_message_text(self, value):
        """
        Validate message text length.
        """
        if len(value) > 1000:
            raise serializers.ValidationError("Message text cannot exceed 1000 characters.")
        if not value.strip():
            raise serializers.ValidationError("Message text cannot be empty.")
        return value


class ActiveUserSerializer(serializers.ModelSerializer):
    """
    Serializer for ActiveUser model.
    """
    class Meta:
        model = ActiveUser
        fields = ['session_id', 'username', 'last_activity']
        read_only_fields = ['last_activity']


class UserRegistrationSerializer(serializers.Serializer):
    """
    Serializer for user registration request.
    """
    session_id = serializers.CharField(max_length=255, required=True)


class UserRegistrationResponseSerializer(serializers.Serializer):
    """
    Serializer for user registration response.
    """
    username = serializers.CharField(max_length=50)
    session_id = serializers.CharField(max_length=255)


class HeartbeatSerializer(serializers.Serializer):
    """
    Serializer for heartbeat request.
    """
    session_id = serializers.CharField(max_length=255, required=True)
    username = serializers.CharField(max_length=50, required=True)


class OnlineCountSerializer(serializers.Serializer):
    """
    Serializer for online users count response.
    """
    online_count = serializers.IntegerField()
