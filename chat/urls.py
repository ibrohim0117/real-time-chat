from django.urls import path
from .views import ChatMessagesList, UserCreateAPIView

urlpatterns = [
    path("messages/<str:room_name>/", ChatMessagesList.as_view(), name="chat-messages"),
    path("user/create/", UserCreateAPIView.as_view(), name="user-create"),
]
