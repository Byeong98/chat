"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from chat.routing import websocket_urlpatterns
from chat.middlewares import JWTAuthMiddleware

application = ProtocolTypeRouter(
    {
        "http": application,
        "websocket": 
            JWTAuthMiddleware(URLRouter(websocket_urlpatterns))
        ,
    }
)
# application = ProtocolTypeRouter(
#     {
#         "http": application,
#         "websocket": 
#                 AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
#         ,
#     }
# )