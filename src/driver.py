from sensors.motor import *
from sensors.colorsensor import *


class Driver:

    # construct objects for the Motor, ColorSensor
    def __init__(self):
        self.motor_control = Motor()
        self.color_sensor = ColorSensor()

    # drive forward for a set time
    def move_straight(self, timef):
        self.motor_control.forward(timef)

    # turns the car while driving by a set amount
    # 3 parameters -> time_t: in ms, speed: initial speed for both wheels,
    # strength: multiplier of speed for the faster wheel
    def turn_right(self, time_t, speed, strength):
        speed_right = speed
        speed_left = speed*strength
        self.motor_control.move_left_right(time_t, speed_left, speed_right)

    # turns the car while driving by a set amount
    # 3 parameters -> time_t: in ms, speed: initial speed for both wheels,
    # strength: multiplier of speed for the faster wheel
    def turn_left(self, time_t, speed, strength):
        speed_left = speed
        speed_right = speed*strength
        self.motor_control.move_left_right(time_t, speed_left, speed_right)

    # main function to follow the line
    def follow_line(self):
        strength_mod = 0
        current_color = 1
        for i in range(0,3000):
            # if the brightness value is less than 150, robot is on black and turns right
            if self.color_sensor.get_avg() < 150:
                if current_color == 1:
                    current_color = 0
                    strength_mod = 0
                self.turn_right(15, 400, 1+(strength_mod//100))
                strength_mod += 1
            # if the brightness value is more than 150, robot is on white and turns left
            elif self.color_sensor.get_avg() >= 150:
                if current_color == 0:
                    current_color = 1
                    strength_mod = 0
                self.turn_left(15, 400, 1+(strength_mod//100))
                strength_mod += 1
            # otherwise just continues next loop (safety)
            else:
                continue
