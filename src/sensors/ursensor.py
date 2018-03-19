import ev3dev.ev3 as ev3

class UsSensor:
    def __init__(self):
        self.usS = ev3.UltrasonicSensor()
        self.usS.mode = 'US-DIST-CM'
    # distance in cm
    distance = usS.value()

    #displays measured data
    def get_value(self):
        print(self.usS.bin_data())
        return self.usS.bin_data('<b')

#for driver.py

from sensors.ursensor import *

    #placeholder distance
     if distance < 50
