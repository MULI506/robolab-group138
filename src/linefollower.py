from sensors.motor import *
from sensors.colorsensor import *


class LineFollower:

    def __init__(self):
        self.motor_control = Motor()
        self.color_sensor = ColorSensor()

    def move_straight(self):
        self.motor_control.forward()

    def turn_left(self, time, speed, strength):
        speed_right = speed
        speed_left = speed*strength
        self.motor_control.move_left_right(time, speed_left, speed_right)

    def turn_right(self, time, speed, strength):
        speed_left = speed
        speed_right = speed*strength
        self.motor_control.move_left_right(time, speed_left, speed_right)

    def turn(self, time, speed, strength):
        speed_right = speed
        speed_left = speed*strength
        self.motor_control.move_left_right(time, speed_left, speed_right)

    def follow_line(self):
        strength_mod = 0
        current_color = 1
        for i in range(0,3000):
            if self.color_sensor.get_avg() < 150:
                if current_color == 1:
                    current_color = 0
                    strength_mod = 0
                self.turn_left(15, 400, 1+(strength_mod//100))
                strength_mod += 1
            elif self.color_sensor.get_avg() >= 150:
                if current_color == 0:
                    current_color = 1
                    strength_mod = 0
                self.turn_right(15, 400, 1+(strength_mod//100))
                strength_mod += 1
            else:
                continue
