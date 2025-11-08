from django.urls import path
from .views import (
    MessageListCreateView,
    UserRegistrationView,
    HeartbeatView,
    OnlineUsersView
)

urlpatterns = [
    path("messages/", MessageListCreateView.as_view(), name="message-list-create"),
    path("users/register/", UserRegistrationView.as_view(), name="user-register"),
    path("users/heartbeat/", HeartbeatView.as_view(), name="user-heartbeat"),
    path("users/online/", OnlineUsersView.as_view(), name="users-online"),
]
