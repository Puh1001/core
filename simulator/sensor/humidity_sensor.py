from .base_sensor import BaseSensor

class HumiditySensor(BaseSensor):
    def __init__(self, sensor_id, is_soil=True):
        super().__init__(
            sensor_id=sensor_id,
            sensor_type="humidity",
            min_value=20 if is_soil else 40,  # Soil humidity: 20-80%, Air humidity: 40-90%
            max_value=80 if is_soil else 90
        )
        self.is_soil = is_soil

    async def read(self):
        reading = await super().read()
        reading["subtype"] = "soil" if self.is_soil else "ambient"
        return reading
