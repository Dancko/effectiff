from django.urls import re_path

from . import consumers


websocket_urlpatterns = [
    re_path(
        r"ws/task/chat/(?P<room_name>[^/]+)/",
        consumers.TaskChatConsumer.as_asgi(),
    ),
]
