import time
import random

class SHT30:
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        temperature = random.uniform(20.0, 30.0)
        humidity = random.uniform(40.0, 60.0)
        
        # time.sleep(0.5)
        
        return temperature, humidity
    
def readSHT30Sensor(pin):
    sensor = SHT30(pin)
    return sensor.read()