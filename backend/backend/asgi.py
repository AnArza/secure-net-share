# """
# ASGI config for backend project.
#
# It exposes the ASGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# """
#
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from backend.profiles.middleware import JWTAuthMiddleware
from backend.profiles.routing import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Define the root routing configuration for Channels
application = ProtocolTypeRouter({
    # HTTP/WebSocket protocol switching
    'http': get_asgi_application(),
    'websocket': JWTAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
