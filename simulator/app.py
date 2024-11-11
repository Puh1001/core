import asyncio
from gateway.sensor_gateway import SensorGateway
from sensor.temperature_sensor import TemperatureSensor
from sensor.humidity_sensor import HumiditySensor
from sensor.light_sensor import LightSensor
from sensor.ph_sensor import PHSensor

async def main():
    # Khởi tạo gateway
    gateway = SensorGateway("gateway_001", "http://localhost:8000")
    
    # Thêm các cảm biến
    sensors = [
        TemperatureSensor("temp_001"), # nhiệt độ đất
        TemperatureSensor("temp_002"), # nhiệt độ không khí
        HumiditySensor("humid_001"), # độ ẩm đất
        HumiditySensor("humid_002"), # độ ẩm không khí
        LightSensor("light_001"), # ánh sáng
        PHSensor("ph_001"), # pH
    ]
    
    for sensor in sensors:
        gateway.add_sensor(sensor)
    
    # Khởi động gateway
    await gateway.start()

if __name__ == "__main__":
    asyncio.run(main())