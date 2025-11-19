import json
import logging
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import ChatRoom, Message, User

logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.group_name = f"notifications_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        logger.info(f"NOTIFICATION: User {self.user.username} connected to notification channel.")

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            logger.info(f"NOTIFICATION: User {self.user.username} disconnected from notification channel.")

    async def chat_notification(self, event):
        logger.info(f"NOTIFICATION: Sending notification to user {self.user.id}. Event: {event}")
        await self.send(text_data=json.dumps({
            'type': 'chat_notification',
            'message': event['message']
        }))

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        self.room, created = await self.get_or_create_room()
        logger.info(f"CHAT: User {self.user.username} connected to room {self.room_name}. Room object: {self.room}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        messages = await self.get_messages()
        logger.info(f"CHAT: Found {len(messages)} historical messages for room {self.room_name}.")

        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message.content,
                'nickname': message.sender.nickname
            }))

    async def disconnect(self, close_code):
        logger.info(f"CHAT: User {self.user.username} disconnected from room {self.room_name}.")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        nickname = self.user.nickname
        
        logger.info(f"CHAT: Received message '{message}' from {self.user.username} in room {self.room_name}.")
        await self.save_message(message)
        logger.info("CHAT: Message saved to DB.")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'nickname': nickname
            }
        )
        
        other_user_id = await self.get_other_user_id()
        if other_user_id:
            logger.info(f"CHAT: Sending notification to user ID {other_user_id}.")
            channel_layer = get_channel_layer()
            await channel_layer.group_send(
                f"notifications_{other_user_id}",
                {
                    "type": "chat.notification",
                    "message": f"'{self.room_name}' 방에서 새 메시지가 도착했습니다.",
                },
            )

    async def chat_message(self, event):
        message = event['message']
        nickname = event['nickname']

        await self.send(text_data=json.dumps({
            'message': message,
            'nickname': nickname
        }))

    @database_sync_to_async
    def get_or_create_room(self):
        return ChatRoom.objects.get_or_create(name=self.room_name)

    @database_sync_to_async
    def get_messages(self):
        if not self.room:
            return []
        recent_messages = self.room.messages.select_related('sender').all().order_by('-timestamp')[:50]
        return list(reversed(recent_messages))

    @database_sync_to_async
    def save_message(self, message):
        if not self.room:
            logger.error(f"CHAT: Could not save message for user {self.user.username} because self.room is not set.")
            return
        Message.objects.create(room=self.room, sender=self.user, content=message)

    @database_sync_to_async
    def get_other_user_id(self):
        try:
            ids_str = self.room.name.split('_')[1]
            user_id_1, user_id_2 = map(int, ids_str.split('-'))
            return user_id_2 if self.user.id == user_id_1 else user_id_1
        except (IndexError, ValueError):
            return None
