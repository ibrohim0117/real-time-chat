from django.urls import path
from .views import SendMessageAPIView

urlpatterns = [
    path("send-message/", SendMessageAPIView.as_view(), name="send-message"),
]
