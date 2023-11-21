import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from chat.consumers import TextRoomConsumer
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>\w+)/$', TextRoomConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
