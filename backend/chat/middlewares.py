from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken, TokenError


user = get_user_model()

@database_sync_to_async
def get_user(user_id):
    try:
        return user.objects.get(id=user_id)
    except user.DoesNotExist:
        return AnonymousUser()
    

class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        authorization_header = next(
            (header for header in scope["headers"] if header[0] == b"cookie"), None
        )

        if authorization_header:
            token = (
                authorization_header[1].decode("utf-8").split("=")[-1]
            )
        else:
            token = None

        try:
            access_token = AccessToken(token)
            scope["user"] = await get_user(access_token["user_id"])
        except TokenError:
            scope["user"] = AnonymousUser()

        print("user : ", scope["user"])

        return await super().__call__(scope, receive, send)