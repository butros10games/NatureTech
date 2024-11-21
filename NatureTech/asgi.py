"""
ASGI config for NatureTech project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from booking_system.routing import websocket_urlpatterns as booking_system_routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NatureTech.settings")
django_asgi_app = get_asgi_application()

all_websocket_urlpatterns = booking_system_routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter(all_websocket_urlpatterns)),
    }
)
