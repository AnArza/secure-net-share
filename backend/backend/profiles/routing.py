from django.urls import path
from backend import consumers

websocket_urlpatterns = [
    path('ws/status/', consumers.UserStatusConsumer.as_asgi()),
    path('ws/files/', consumers.FileConsumer.as_asgi())
]
