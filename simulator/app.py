import asyncio
from gateway.sensor_gateway import SensorGateway
from sensor.temperature_sensor import TemperatureSensor
from sensor.humidity_sensor import HumiditySensor

async def main():
    # Khởi tạo gateway
    gateway = SensorGateway("gateway_001", "http://localhost:8000")
    
    # Thêm các cảm biến
    sensors = [
        TemperatureSensor("temp_001"),
        TemperatureSensor("temp_002"),
        HumiditySensor("humid_001")
    ]
    
    for sensor in sensors:
        gateway.add_sensor(sensor)
    
    # Khởi động gateway
    await gateway.start()

if __name__ == "__main__":
    asyncio.run(main())