from .base_sensor import BaseSensor

class LightSensor(BaseSensor):
    def __init__(self, sensor_id):
        super().__init__(
            sensor_id=sensor_id,
            sensor_type="light",
            min_value=0,    # Light intensity in lux (0-100000)
            max_value=100000
        )

    async def read(self):
        reading = await super().read()
        reading["unit"] = "lux"
        return reading
