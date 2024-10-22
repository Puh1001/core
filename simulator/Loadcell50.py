import time
import random

class Loadcell50:
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        weight = random.uniform(5.0, 50.0)
        # time.sleep(0.5)
        return weight
    
def readLoadCellSensor(pin):
    sensor = Loadcell50(pin)
    return sensor.read()