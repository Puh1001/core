import asyncio
import json
import aiohttp
import logging
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SensorGateway:
    def __init__(self, gateway_id, server_url):
        self.gateway_id = gateway_id
        self.server_url = server_url
        self.sensors = {}
        self.sensor_data = defaultdict(dict)
        self.reading_interval = 1  # seconds
        self._is_running = False
        
    def add_sensor(self, sensor):
        """Thêm cảm biến vào gateway"""
        self.sensors[sensor.sensor_id] = sensor
        logger.info(f"Added sensor {sensor.sensor_id} to gateway {self.gateway_id}")
        
    async def read_sensors(self):
        """Đọc dữ liệu từ tất cả các cảm biến"""
        readings = []
        for sensor in self.sensors.values():
            try:
                reading = await sensor.read()
                readings.append(reading)
                self.sensor_data[sensor.sensor_id] = reading
            except Exception as e:
                logger.error(f"Error reading sensor {sensor.sensor_id}: {e}")
        return readings
    
    async def send_data_to_server(self, data):
        """Gửi dữ liệu lên máy chủ"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "gateway_id": self.gateway_id,
                    "readings": data
                }
                async with session.post(
                    f"{self.server_url}/api/sensor-data",
                    json=payload
                ) as response:
                    if response.status != 200:
                        logger.error(f"Error sending data: {await response.text()}")
        except Exception as e:
            logger.error(f"Connection error: {e}")
            
    async def start(self):
        """Khởi động gateway"""
        self._is_running = True
        logger.info(f"Gateway {self.gateway_id} started")
        
        while self._is_running:
            try:
                # Đọc dữ liệu từ tất cả cảm biến
                readings = await self.read_sensors()
                
                # Gửi dữ liệu lên server
                if readings:
                    await self.send_data_to_server(readings)
                    
                # Đợi đến chu kỳ đọc tiếp theo
                await asyncio.sleep(self.reading_interval)
                
            except Exception as e:
                logger.error(f"Gateway error: {e}")
                await asyncio.sleep(5)  # Đợi 5 giây trước khi thử lại
                
    def stop(self):
        """Dừng gateway"""
        self._is_running = False
        logger.info(f"Gateway {self.gateway_id} stopped")