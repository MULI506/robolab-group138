from sensors.motor import *
from sensors.colorsensor import *

class Driver:

    # construct objects for the Motor, ColorSensor
    def __init__(self):
        self.motor_control = Motor()
        self.color_sensor = ColorSensor()


    # drive forward for a set time
    def move_straight(self, time):
        self.motor_control.forward(time)

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

    # p controller returns modifier for speed reduction during turns
    def p_control(self):
        # maximum degree of speed reduction - 1
        max_modifier = 2
        # get brightness value from color sensor
        brightness = self.color_sensor.get_avg()
        # limit brightness range
        if brightness > 210:
            brightness = 210
        elif brightness < 30:
            brightness = 30

        # measured values for detected black- and white-values
        black = 30
        white = 210
        # determine crossover-value between black and white
        grey_value = (black+white)//2  # 120
        # range of values for each side (black to grey/white to grey)
        prop_range = white - grey_value
        # slope of linear function
        kp_factor = (max_modifier - (-max_modifier)) / ((-prop_range) - prop_range)  # -0.02222
        ### print(kp_factor)
        # difference between middle value and current value of brightness
        error = brightness - grey_value
        #
        turn_modifier = 1 + (kp_factor * error)
        ### print(turn_modifier)
        return turn_modifier

    # turns the car while driving by a set amount using P-controller
    # 3 parameters -> time_t: in ms, speed: initial speed for both wheels,
    # modifier: determines direction and degree of speed reduction for slower wheel
    def turn_control(self, time_t, speed, modifier):
        # right turn: slow down left wheel
        if modifier > 0:
            speed_right = speed
            speed_left = int(speed/modifier)
        # left turn: slow down right wheel
        elif modifier <= 0:
            speed_left = speed
            speed_right = int(speed/(-modifier))
        else:
            speed_left = speed
            speed_right = speed

        self.motor_control.move_left_right(time_t, speed_left, speed_right)


    # main function to follow the line
    def follow_line(self):
        time_each_move = 20
        max_speed = 500
        for i in range(0, 3000):
            turn_modifier = self.p_control()
            self.turn_control(time_each_move, max_speed, turn_modifier)
