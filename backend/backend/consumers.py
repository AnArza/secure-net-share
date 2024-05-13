from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async

from backend.profiles.models import UserProfile
from backend.profiles.serializers import UserProfileSerializer
from backend.file_management.models import File
from backend.file_management.serializers import FileSerializer

class UserStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add('active_users', self.channel_name)
        await self.send_active_users()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('active_users', self.channel_name)

    async def send_active_users(self):
        active_users = await self.get_active_users()
        await self.send(text_data=json.dumps({
            'type': 'active_users',
            'users': active_users
        }))

    @database_sync_to_async
    def get_active_users(self):
        active_users = UserProfile.objects.filter(is_online=True).exclude(user=self.scope['user'])
        return UserProfileSerializer(active_users, many=True).data

    async def user_status_change(self, event):
        await self.send_active_users()


class FileConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.file_filter_users = [self.scope['user'].id]
        await self.channel_layer.group_add('file_updates', self.channel_name)
        await self.send_user_files()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('file_updates', self.channel_name)

    async def send_user_files(self):
        files = await self.get_filtered_files()
        await self.send(text_data=json.dumps({
            'type': 'files_list',
            'files': files
        }))

    @database_sync_to_async
    def get_filtered_files(self):
        self.file_filter_users = [self.scope['user'].id]
        files = File.objects.filter(owner__id__in=self.file_filter_users)
        return FileSerializer(files, many=True).data

    async def file_uploaded(self, event):
        if event['file']['owner']['id'] in self.file_filter_users:
            await self.send(text_data=json.dumps({
                'type': 'file_uploaded',
                'file': event['file']
            }))

    async def file_deleted(self, event):
        await self.send(text_data=json.dumps({
            'type': 'file_deleted',
            'file_id': event['file_id']
        }))

    async def file_updated(self, event):
        await self.send(text_data=json.dumps({
            'type': 'file_updated',
            'data': event['files']  # Sending the file data received from the event
        }))
