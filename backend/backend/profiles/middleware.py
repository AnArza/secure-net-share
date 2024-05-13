from urllib.parse import parse_qs
from django.contrib.auth.models import AnonymousUser, User
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

@database_sync_to_async
def get_user(username):
    return User.objects.get(username=username)


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope['query_string'].decode())
        username = query_string.get('username', [None])[0]
        if username:
            scope['user'] = await get_user(username)
        else:
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)
