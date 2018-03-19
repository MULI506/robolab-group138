from sensors.motor import *
from sensors.colorsensor import *
from sounds import *


class Driver:

    # construct objects for the Motor, ColorSensor
    def __init__(self):
        self.motor_control = Motor()
        self.color_sensor = ColorSensor()
        self.sounds = Sounds()

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

    # turns the robot on the spot - about 180°
    def turn_around(self):
        time_r = 1000
        speed = 350
        self.motor_control.move_left_right(time_r, -speed, speed)

    def stop_robot(self):
        self.motor_control.stop()

    # p controller returns modifier for speed reduction during turns
    def p_control(self, brightness):
        # maximum degree of speed reduction - 1
        max_modifier = 2
        #print("bright = {}".format(brightness))
        # limit brightness range
        if brightness > 305:
            brightness = 305
        elif brightness < 35:
            brightness = 35

        # measured values for detected black- and white-values
        black = 35
        white = 305
        # determine crossover-value between black and white
        grey_value = (black+white)//2  # 120
        # range of values for each side (black to grey/white to grey)
        prop_range = white - grey_value
        # slope of linear function
        kp_factor = (max_modifier - (-max_modifier)) / ((-prop_range) - prop_range)  # -0.02222
        #print("KP = {}".format(kp_factor))
        # difference between middle value and current value of brightness
        error = brightness - grey_value
        #print("error = {}".format(error))
        if error > 0:
            turn_modifier = -1 + (kp_factor * error)
        else:
            turn_modifier = 1 + (kp_factor * error)
        print("TM = {}".format(turn_modifier))
        return turn_modifier

    # turns the car while driving by a set amount using P-controller
    # 3 parameters -> time_t: in ms, speed: initial speed for both wheels,
    # modifier: determines direction and degree of speed reduction for slower wheel
    def turn_control(self, time_t, speed, modifier):
        # right turn: slow down left wheel
        if modifier <= 0:
            speed_right = speed
            speed_left = int(speed/-modifier)
        # left turn: slow down right wheel
        elif modifier > 0:
            speed_left = speed
            speed_right = int(speed/(modifier))
        else:
            speed_left = speed
            speed_right = speed

        #print("Speed_L = {}".format(speed_left))
        #print("Speed_R = {}".format(speed_right))

        #self.motor_control.move_left_right(time_t, speed_left, speed_right)
        self.motor_control.move_lr_steady(speed_left, speed_right)

    def turn_control_steady(self, speed, modifier):
        # right turn: slow down left wheel
        if modifier <= 0:
            speed_right = speed
            speed_left = int(speed/-modifier)
        # left turn: slow down right wheel
        elif modifier > 0:
            speed_left = speed
            speed_right = int(speed/(modifier))
        else:
            speed_left = speed
            speed_right = speed

        #print("Speed_L = {}".format(speed_left))
        #print("Speed_R = {}".format(speed_right))

        self.motor_control.move_lr_steady(speed_left, speed_right)


    # main function to follow the line
    def follow_line(self):
        time_each_move = 100
        max_speed = 200

        self.motor_control.reset_position()
        print(self.motor_control.get_position())
        for i in range(0, 3000):
            color = self.color_sensor.get_color()
            if color == 'red':
                self.sounds.say_red()
                break
            if color == 'blue':
                self.sounds.say_blue()
                break
            else:
                turn_modifier = self.p_control(color)
                self.turn_control(time_each_move, max_speed, turn_modifier)
                print(self.motor_control.get_position())

    def follow_line_steady(self):
        max_speed = 300
        for i in range(0, 3000):
            turn_modifier = self.p_control()
            self.turn_control_steady(max_speed, turn_modifier)
