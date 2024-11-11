from .base_sensor import BaseSensor
import random
class PHSensor(BaseSensor):
    def __init__(self, sensor_id):
        super().__init__(
            sensor_id=sensor_id,
            sensor_type="ph",
            min_value=0,    # pH scale 0-14
            max_value=14
        )

    def generate_reading(self):
        # pH readings typically don't fluctuate as much as other sensors
        base_value = super().generate_reading()
        # Reduce noise for pH readings
        noise = random.uniform(-0.05, 0.05)
        return round(base_value + noise, 2)