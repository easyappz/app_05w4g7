from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiResponse
import random

from .models import Message, ActiveUser
from .serializers import (
    MessageSerializer,
    UserRegistrationSerializer,
    UserRegistrationResponseSerializer,
    HeartbeatSerializer,
    OnlineCountSerializer
)


class MessageListCreateView(APIView):
    """
    API endpoint for listing all messages and creating new messages.
    """

    @extend_schema(
        responses={200: MessageSerializer(many=True)},
        description="Get all chat messages ordered by timestamp"
    )
    def get(self, request):
        """
        Retrieve all chat messages ordered by timestamp (ascending).
        """
        messages = Message.objects.all().order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=MessageSerializer,
        responses={
            201: MessageSerializer,
            400: OpenApiResponse(description="Bad request - validation error")
        },
        description="Create a new chat message"
    )
    def post(self, request):
        """
        Create a new message.
        """
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegistrationView(APIView):
    """
    API endpoint for registering a session user with auto-generated username.
    """

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={
            200: UserRegistrationResponseSerializer,
            201: UserRegistrationResponseSerializer,
            400: OpenApiResponse(description="Bad request - validation error")
        },
        description="Register a session user and get auto-generated username"
    )
    def post(self, request):
        """
        Register a session user. Generate random username in format 'Гость-XXXX'.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        session_id = serializer.validated_data['session_id']
        
        # Check if user already exists
        try:
            active_user = ActiveUser.objects.get(session_id=session_id)
            response_serializer = UserRegistrationResponseSerializer({
                'username': active_user.username,
                'session_id': active_user.session_id
            })
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ActiveUser.DoesNotExist:
            pass

        # Generate unique username
        username = self._generate_username()
        
        # Create new active user
        active_user = ActiveUser.objects.create(
            session_id=session_id,
            username=username
        )
        
        response_serializer = UserRegistrationResponseSerializer({
            'username': active_user.username,
            'session_id': active_user.session_id
        })
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def _generate_username(self):
        """
        Generate random username in format 'Гость-XXXX' where XXXX is a 4-digit number.
        """
        while True:
            random_number = random.randint(1000, 9999)
            username = f"Гость-{random_number}"
            # Check if username is unique
            if not ActiveUser.objects.filter(username=username).exists():
                return username


class HeartbeatView(APIView):
    """
    API endpoint for updating user activity.
    """

    @extend_schema(
        request=HeartbeatSerializer,
        responses={
            200: OpenApiResponse(description="Activity updated successfully"),
            400: OpenApiResponse(description="Bad request - validation error"),
            404: OpenApiResponse(description="User not found")
        },
        description="Update user activity timestamp"
    )
    def post(self, request):
        """
        Update user activity timestamp.
        """
        serializer = HeartbeatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        session_id = serializer.validated_data['session_id']
        username = serializer.validated_data['username']

        try:
            active_user = ActiveUser.objects.get(session_id=session_id)
            active_user.username = username
            active_user.save()  # This will update last_activity due to auto_now=True
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except ActiveUser.DoesNotExist:
            # Create user if doesn't exist
            ActiveUser.objects.create(
                session_id=session_id,
                username=username
            )
            return Response({"status": "created"}, status=status.HTTP_200_OK)


class OnlineUsersView(APIView):
    """
    API endpoint for getting count of online users.
    """

    @extend_schema(
        responses={200: OnlineCountSerializer},
        description="Get count of online users (active in last 5 minutes)"
    )
    def get(self, request):
        """
        Get count of online users (users active in last 5 minutes).
        """
        # Cleanup inactive users before counting
        ActiveUser.cleanup_inactive_users()
        
        online_count = ActiveUser.get_online_count()
        serializer = OnlineCountSerializer({'online_count': online_count})
        return Response(serializer.data)
