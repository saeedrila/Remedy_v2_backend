import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from chat.consumers import TextRoomConsumer
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack


websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>\w+)/$', TextRoomConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
