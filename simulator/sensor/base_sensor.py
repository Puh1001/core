#sensor/base_sensor.py
import random
import time
import asyncio

class BaseSensor:
    def __init__(self, sensor_id, sensor_type, min_value, max_value):
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.min_value = min_value
        self.max_value = max_value
        self._is_running = False
        
    def generate_reading(self):
        base_value = random.uniform(self.min_value, self.max_value)
        noise = random.uniform(-0.1, 0.1) * base_value
        return round(base_value + noise, 2)
    
    async def read(self):
        return {
            "sensor_id": self.sensor_id,
            "type": self.sensor_type,
            "value": self.generate_reading(),
            "timestamp": time.time()
        }
