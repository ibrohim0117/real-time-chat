from django.urls import path
from .views import SendMessageAPIView, UserMessagesAPIView, RegisterUserAPIView, LoginAPIView

urlpatterns = [
    path("send-message/", SendMessageAPIView.as_view(), name="send-message"),
    path("messages/", UserMessagesAPIView.as_view(), name="user-messages"),

    path("register/", RegisterUserAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),

]
