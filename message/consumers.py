import json
import logging
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        self.room, created = await self.get_or_create_room()
        logger.info(f"User {self.user.username} connected to room {self.room_name}. Room object: {self.room}")

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        messages = await self.get_messages()
        logger.info(f"Found {len(messages)} historical messages for room {self.room_name}.")

        for message in messages:
            logger.info(f"Sending historical message from {message.sender.username}: {message.content}")
            await self.send(text_data=json.dumps({
                'message': message.content,
                'nickname': message.sender.nickname  # Use nickname
            }))

    async def disconnect(self, close_code):
        logger.info(f"User {self.user.username} disconnected from room {self.room_name}.")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        nickname = self.user.nickname  # Use nickname
        
        logger.info(f"Received message '{message}' from {self.user.username} in room {self.room_name}. Preparing to save.")
        await self.save_message(message)
        logger.info("Message saved to DB.")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'nickname': nickname  # Use nickname
            }
        )

    async def chat_message(self, event):
        message = event['message']
        nickname = event['nickname']  # Use nickname

        await self.send(text_data=json.dumps({
            'message': message,
            'nickname': nickname  # Use nickname
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
            logger.error(f"Could not save message for user {self.user.username} because self.room is not set.")
            return
        Message.objects.create(room=self.room, sender=self.user, content=message)
