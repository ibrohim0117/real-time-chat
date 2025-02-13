from django.urls import path
from .views import ChatMessagesList

urlpatterns = [
    path("messages/<str:room_name>/", ChatMessagesList.as_view(), name="chat-messages"),
]
