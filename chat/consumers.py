# app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatMessage
from authentication.models import Account
from channels.db import database_sync_to_async


class TextRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('Reached TextRoomConsumer Connect')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_account_instance(self, account_id):
        return Account.objects.get(id=account_id)

    async def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        text = text_data_json['text']
        sender = text_data_json['sender']
        reciever = text_data_json['reciever']

        sender_instance = await self.get_account_instance(sender)
        reciever_instance = await self.get_account_instance(reciever)

        # Have to take Account instance
        chat_message_instance = await self.save_message(sender_instance, reciever_instance, self.room_name, text)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'id': chat_message_instance.id,
                'message': text,
                'sender': sender,
                'reciever': reciever,
            }
        )

    async def chat_message(self, event):
        # Receive message from room group
        message_id = event['id']
        text = event['message']
        sender = event['sender']
        reciever = event['reciever']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'id': message_id,
            'message': text,
            'sender': sender,
            'reciever': reciever,
        }))

    @database_sync_to_async
    def save_message(self, sender, reciever, room, message):
        return ChatMessage.objects.create(sender=sender, reciever=reciever, room=room, message=message)