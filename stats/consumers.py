from channels.generic.websocket import AsyncWebsocketConsumer
import json
import re
from channels.db import database_sync_to_async
from .models import Plot, RealStats
from urllib.parse import unquote

class StatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        name = self.scope['url_route']['kwargs']['name']
        self.name = unquote(name)
        print(f"Connecting to plot: {self.name}")
        # Sanitize the group name
        self.group_name = re.sub(r'[^a-zA-Z0-9_-]', '_', f'stats_{self.name}')
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("disconnected", close_code)
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = text_data_json['sender']
        print("received", message, sender)

        await self.save_data_item(sender, message, self.name)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_message',
                'message': message,
                'sender': sender
            }
        )
    
    async def send_message(self, event):
        message = event['message']
        sender = event['sender']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    @database_sync_to_async    
    def create_data_item(self, sender, message, name):
        try:
            obj = Plot.objects.get(name=name)
            return RealStats.objects.create(plot=obj, sender=sender, message=message)
        except Plot.DoesNotExist:
            print(f"Plot with name '{name}' does not exist.")
            return None

    async def save_data_item(self, sender, message, name):
        await self.create_data_item(sender, message, name)