import time
import random

class pH:
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        ph = random.uniform(3.0, 9.0)
        # time.sleep(0.5)
        return ph
    
def readpHSensor(pin):
    sensor = pH(pin)
    return sensor.read()