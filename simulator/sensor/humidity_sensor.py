from .base_sensor import BaseSensor

class HumiditySensor(BaseSensor):
    def __init__(self, sensor_id, min_humidity=40, max_humidity=80):
        super().__init__(sensor_id, "humidity", min_humidity, max_humidity)