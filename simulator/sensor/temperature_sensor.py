# sensor/temperature_sensor.py
from .base_sensor import BaseSensor

class TemperatureSensor(BaseSensor):
    def __init__(self, sensor_id, is_soil=True):
        super().__init__(
            sensor_id=sensor_id,
            sensor_type="temperature",
            min_value=15 if is_soil else 20,  # Soil temp range: 15-35°C, Air temp range: 20-40°C
            max_value=35 if is_soil else 40
        )
        self.is_soil = is_soil

    async def read(self):
        reading = await super().read()
        reading["subtype"] = "soil" if self.is_soil else "ambient"
        return reading