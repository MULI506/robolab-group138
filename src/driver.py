from sensors.motor import *
from sensors.colorsensor import *
from sensors.ursensor import *
from odometry import *
from sounds import *

import time
import math

class Driver:

    # construct objects for the Motor, ColorSensor
    def __init__(self):
        self.motor_control = Motor()
        self.color_sensor = ColorSensor()
        self.sounds = Sounds()
        self.odo = Odometry()
        self.us_sensor = UsSensor()

        self.position_known = (0, 0)
        self.rotation_known = 0
        self.path_status = 'free'

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
        self.motor_control.wait()

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
        grey_value = (black+white)//2  # 170
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

        self.motor_control.move_left_right(time_t, speed_left, speed_right)
        #self.motor_control.move_lr_steady(speed_left, speed_right)

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

    # follow the line using a timed motor run
    def follow_line(self):
        time_each_move = 15
        max_speed = 400

        self.motor_control.reset_position()
        print(self.motor_control.get_position())
        for i in range(0, 3000):
            color = self.color_sensor.get_color()
            if color == 'red':
                self.motor_control.stop()
                self.sounds.say_red()
                time.sleep(1)
                self.motor_control.forward(1000)

            if color == 'blue':
                self.motor_control.stop()
                self.sounds.say_blue()
                time.sleep(1)
                self.motor_control.forward(1000)
            else:
                turn_modifier = self.p_control(int(color))
                self.turn_control(time_each_move, max_speed, turn_modifier)
                print(self.motor_control.get_position())

    # follow line
    def follow_line_steady(self):
        max_speed = 300
        for i in range(0, 3000):
            turn_modifier = self.p_control()
            self.turn_control_steady(max_speed, turn_modifier)

    # follow line using preset turn values
    def follow_line_simple(self):
        max_speed = 500
        strength = 2
        time_step = 15
        for i in range(0, 3000):
            brightness = self.color_sensor.get_avg()
            if brightness >= 170:
                speed_right = 600
                speed_left = 300
            elif brightness < 170:
                speed_left = 600
                speed_right = 300
            else:
                speed_left = 300
                speed_right = 300
            self.motor_control.move_left_right(time_step, speed_left, speed_right)

    # p-value using addition-modifier
    def p_control_add(self, brightness, mod):
        # maximum degree of speed reduction - 1
        max_modifier = mod
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
        grey_value = (black+white)//2  # 170
        # range of values for each side (black to grey/white to grey)
        prop_range = white - grey_value
        # slope of linear function
        kp_factor = (max_modifier - (-max_modifier)) / ((-prop_range) - prop_range)  # -0.02222
        #print("KP = {}".format(kp_factor))
        # difference between middle value and current value of brightness
        error = brightness - grey_value
        #print("error = {}".format(error))
        if error > 0:
            turn_modifier = (kp_factor * error)
        else:
            turn_modifier = (kp_factor * error)
        # print("TM = {}".format(turn_modifier))
        return int(turn_modifier)

    # follow line using addition modifier
    def follow_line_add(self, intime, inspeed, inmod):
        time_each_move = intime
        max_speed = inspeed

        self.motor_control.reset_position()
        print(self.motor_control.get_position())
        for i in range(0, 3000):
            color = self.color_sensor.get_color()
            if color == 'red':
                self.motor_control.stop()
                self.sounds.say_red()
                time.sleep(1)
                self.motor_control.forward(1000)

            elif color == 'blue':
                self.motor_control.stop()
                self.sounds.say_blue()
                time.sleep(1)
                self.motor_control.forward(1000)
            else:
                print(self.us_sensor.get_value())
                if self.us_sensor.get_value() < 140:
                    self.motor_control.stop()
                    self.sounds.say_oooo()
                    self.turn_around()
                turn_modifier = self.p_control_add(int(color), inmod)
                self.turn_control_add(time_each_move, max_speed, turn_modifier)
                #print(self.motor_control.get_position())

    # control a turn using addition modifier
    def turn_control_add(self, speed, modifier):
        # right turn: slow down left wheel
        speed_left = speed + modifier
        speed_right = speed - modifier

        #print("Speed_L = {}".format(speed_left))
        #print("Speed_R = {}".format(speed_right))

        #self.motor_control.move_left_right(time_t, speed_left, speed_right)
        self.motor_control.move_lr_steady(speed_left, speed_right)



    # test odometry data for repetitive small movements
    def odometry_test(self, axis, diameter, sleeptime):
        self.odo.set_step_distance(diameter)
        self.motor_control.free_motor()
        self.motor_control.reset_position()
        self.rotation_known = 0
        self.position_known = (0, 0)
        self.odo.set_current_position((0, 0))
        self.odo.set_current_rotation(0)
        i = 0
        while True:
            i += 1
            self.odometry_step_old(sleeptime, axis, i)

            color = self.color_sensor.get_color()
            if color == 'red':
                break
            elif color == 'blue':
                break
            else:
                continue
        position_guess = self.odo.guess_position(self.position_known)
        #guess_coord = position_guess[0]
        #guess_rot = position_guess[1]
        #self.sounds.say_coordinate(guess_coord, guess_rot)


    def odometry_step_old(self, sleeptime, axis, i):
        wheel_position = self.motor_control.get_position()
        self.motor_control.reset_position()
        odo_data = self.odo.calculate_new_position(wheel_position)
        #position_robot = odo_data[0]
        #rotation = odo_data[1]
        if i % 10 == 0:
           print("position: ({},{}), rotation: {}".format(int(position_robot[0]), int(position_robot[1]), int(rotation)))
        time.sleep(sleeptime)

    # calculates new odometry data each loop
    def odometry_step(self):
        wheel_position = self.motor_control.get_position()
        self.motor_control.reset_position()
        odo_data = self.odo.calculate_new_position(wheel_position)
        #position_robot = odo_data[0]
        #rotation = odo_data[1]
        #if i % 10 == 0:
        #   print("position: ({},{}), rotation: {}".format(int(position_robot[0]), int(position_robot[1]), int(rotation)))
        #time.sleep(sleeptime)

    # follows line from start to finish, considers obstacles
    def follow_line_complete(self, start_position, start_rotation):
        # initialize line following
        set_speed = 120
        set_speed_modifier = 100

        self.motor_control.brake_motor()
        self.motor_control.reset_position()

        self.path_status = 'free'

        # later input values from current location
        self.rotation_known = start_rotation
        self.position_known = start_position
        # reset odometry data
        self.odo.set_current_position((0, 0))
        self.odo.set_current_rotation(0)

        # loop while following line
        while True:
            color = self.color_sensor.get_color()
            if color == 'red':
                self.motor_control.stop()
                self.sounds.say_red()
                break
            elif color == 'blue':
                self.motor_control.stop()
                self.sounds.say_blue()
                break
            else:
                # check for obstacle
                # print(self.us_sensor.get_value())
                if self.us_sensor.get_value() < 140:
                    self.motor_control.stop()
                    self.sounds.say_obstacle()
                    self.turn_around()
                    self.path_status = 'blocked'
                self.odometry_step()
                # control motors and set speeds
                turn_modifier = self.p_control_add(int(color), set_speed_modifier)
                self.turn_control_add(set_speed, turn_modifier)
                # print(self.motor_control.get_position())

        # end of line reached
        new_position = self.odo.guess_position(self.position_known)
        time.sleep(1)
        self.motor_control.forward(1500, 360)


    """"
    TESTFUNCTIONS CURRENTLY UNUSED
    # test odometry data for a single movement
    def odometry_test_simple(self, axis):
        #self.motor_control.forward(time, speed)
        #self.motor_control.move_left_right(1000, 300, 100)
        self.motor_control.free_motor()
        self.motor_control.reset_position()
        rotation = 0
        print("Start WheelPos: {}".format(self.motor_control.get_position()))
        print("Start Rotation: {}".format(rotation))

        time.sleep(6)

        wheel_position = self.motor_control.get_position()

        diff_left = wheel_position[0]
        diff_right = wheel_position[1]
        #print("left: {}, right: {}".format(diff_left, diff_right))

        odo_data = self.odo.calculate_new_position(wheel_position, rotation, axis)
        position = odo_data[0]
        rotation = odo_data[1]
        print("New WheelPos: {}".format(wheel_position))
        print("New coordinates: {}".format(position))
        print("New rotation: {}".format(rotation))
        self.motor_control.brake_motor()
    
    def odometry_step_single(self, sleeptime, axis, i):
        wheel_position = self.motor_control.get_position()
        self.motor_control.reset_position()
        odo_data = self.odo.calculate_new_position(wheel_position, position_robot, math.radians(rotation), axis)
        position_robot = odo_data[0]
        rotation = odo_data[1]
        if i % 10 == 0:
            print(
                "position: ({},{}), rotation: {}".format(int(position_robot[0]), int(position_robot[1]), int(rotation)))
        time.sleep(sleeptime)
    """

