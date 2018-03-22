import ev3dev.ev3 as ev3
import time


class ColorSensor:

    # constructor: setup input for ColorSensor and set mode to RGB-RAW
    def __init__(self):
        self.colorS = ev3.ColorSensor('in2')
        self.colorS.mode = 'RGB-RAW'

    # set the color mode
    # 1 parameter -> new_mode (string value): set new color mode
    def set_mode(self, new_mode):
        self.colorS.mode = new_mode

    # return the current detected color value as rgb-triplet
    # as tuple in format: (red, green, blue)
    def get_value(self):
        print(self.colorS.bin_data())
        return self.colorS.bin_data("hhh")

    # returns color
    # if red or blue -> returns color as string "red" or "blue"
    # if black or white -> returns color as average brightness
    def get_color(self):
        rgb = self.colorS.bin_data("hhh")
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]

        if red > 150 and green < 100 and blue < 100:
            return 'red'
        if red < 100 and blue > 100:
            return 'blue'
        else:
            return self.get_avg()

    # returns the current brightness value disregarding specific colors
    def get_avg(self):
        rgb = self.colorS.bin_data("hhh")
        avg = (rgb[0] + rgb[1] + rgb[2])//3
        return avg

    # test-function to print 1000 detected RGB-values
    def print_values(self):
        # loops 1000 times
        for i in range(0, 1000):
            self.colorS.mode = 'RGB-RAW'
            print(self.colorS.bin_data("hhh"))
            # pauses for 100ms
            time.sleep(.1)
