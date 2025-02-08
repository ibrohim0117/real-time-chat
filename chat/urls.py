from django.urls import path
from .views import SendMessageAPIView, UserMessagesAPIView

urlpatterns = [
    path("send-message/", SendMessageAPIView.as_view(), name="send-message"),
    path("messages/", UserMessagesAPIView.as_view(), name="user-messages"),
]
