from .base_sensor import BaseSensor

class TemperatureSensor(BaseSensor):
    def __init__(self, sensor_id, min_temp=20, max_temp=30):
        super().__init__(sensor_id, "temperature", min_temp, max_temp)