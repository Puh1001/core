from channels.generic.websocket import AsyncWebsocketConsumer
import json
import re
from channels.db import database_sync_to_async
from .models import Plot, RealStats
from urllib.parse import unquote
import requests

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

        # Kiểm tra chỉ số pH và gọi API đóng/mở tank
        data = json.loads(message)
        ph_value = data.get('soilPh')
        if ph_value is not None:
            await self.control_tank_based_on_ph(ph_value)

        # Lưu dữ liệu vào RealStats
        await self.save_real_stats(data)

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
    def control_tank_based_on_ph(self, ph_value):
        try:
            ph_value = float(ph_value)  # Chuyển đổi ph_value sang số thực
        except ValueError:
            print("Invalid pH value:", ph_value)
            return

        if ph_value < 5.5:
            action = 'open'
        elif ph_value > 7.5:
            action = 'close'
        else:
            return

        response = requests.post('http://localhost:8000/stats/control-tank/', data={'tank_id': 1, 'action': action})
        print(response.json())

    @database_sync_to_async
    def save_real_stats(self, data):
        plot = Plot.objects.get(name=self.name)
        RealStats.objects.create(
            plot=plot,
            light=data.get('light', 0),
            ambientTemperature=data.get('ambientTemperature', 0),
            ambientHumidity=data.get('ambientHumidity', 0),
            soilMoistur=data.get('soilMoistur', 0),
            soilTemperature=data.get('soilTemperature', 0),
            soilPh=data.get('soilPh', 0)
        )