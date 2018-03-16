import ev3dev.ev3 as ev3

import time


class ColorSensor:

    def __init__(self):
        self.colorS = ev3.ColorSensor('in2')

    def set_mode(self, new_mode):
        self.colorS.mode = new_mode

    def get_value(self):
        self.colorS.mode = 'RGB-RAW'
        print(self.colorS.bin_data())
        return self.colorS.bin_data()

    def print_values(self):
        for i in range(0,1000):
            self.colorS.mode = 'RGB-RAW'
            print(self.colorS.bin_data("hhh"))
            time.sleep(.1)
