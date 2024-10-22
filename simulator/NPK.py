import time
import random
class NPK:
    def __init__(self, pin):
        self.pin = pin
    def read(self):
        nitro = random.uniform(5.0, 50.0)
        photpho = random.uniform(0.0, 60.0)
        kali = random.uniform(50.0, 300.0)
        # time.sleep(0.5)
        
        return nitro, photpho, kali

def readNPKSensor(pin):
    sensor = NPK(pin)
    return sensor.read()