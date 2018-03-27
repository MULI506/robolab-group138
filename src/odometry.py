# Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters

from typing import List, Optional, Tuple, Dict
import math

class Odometry():

    def __init__(self):
        # setup values for position and rotation
        self.current_position = (0, 0)
        self.current_rotation = 0  # in degrees

        # setup wheel diameter and wheel separation
        self.wheel_dia = 55
        self.wheel_axis = 110  #measured middle: 120mm, 105-110 better
        # calculate how far the wheel moves each degree
        self.step_distance = self.wheel_dia * math.pi / 360

    def get_current_position(self):
        return self.current_position

    def set_current_position(self, position: Tuple[int, int]):
        self.current_position = position

    def get_current_rotation(self):
        return self.current_rotation

    def set_current_rotation(self, rotation):
        self.current_rotation = rotation

    def set_step_distance(self, wheel_diameter):
        self.step_distance = wheel_diameter * math.pi / 360

    def set_axis_separation(self, length):
        self.wheel_axis = length

    def reset_axis_separation(self):
        self.wheel_axis = 110

    # keep the rotation between 0 and 360 degrees
    def limit_rotation_degree(self, rot_deg):
        return rot_deg % 360

    # returns direction as string
    def guess_direction(self, rotation):
        if 0 <= rotation < 45 or rotation >= 315:
            return 'NORTH'
        elif 45 <= rotation < 135:
            return 'WEST'
        elif 135 <= rotation < 225:
            return 'SOUTH'
        elif 225 <= rotation < 315:
            return 'EAST'
        else:
            return 'ERROR'

    # returns direction as number to use for list-index
    def guess_direction_int(self, rotation):
        # NORTH
        if 0 <= rotation < 45 or rotation >= 315:
            return 0
        # WEST
        elif 45 <= rotation < 135:
            return 1
        # SOUTH
        elif 135 <= rotation < 225:
            return 2
        # EAST
        elif 225 <= rotation < 315:
            return 3
        # ERROR
        else:
            return -1

    # guess the new coordinate and rotation/direction of the robot
    def guess_position(self, coordinate_old):
        # COORDINATE
        # distance between nodes in mm
        grid_size = 500
        x_change_grid = - round(self.current_position[1] / grid_size)
        y_change_grid = round(self.current_position[0] / grid_size)

        #print("x_change: {}, y_change: {}".format(x_change_grid, y_change_grid))

        # coordinate changes added to old coordinates
        x_guess = coordinate_old[0] + x_change_grid
        y_guess = coordinate_old[1] + y_change_grid
        # new coordinates as tuple
        coordinate_guess = (x_guess, y_guess)
        #print("old_c: {}, guess_c: {}".format(coordinate_old, coordinate_guess))

        # ROTATION
        rot_guess = self.current_rotation
        #print("rotation: measured {}, guessed {}".format(int(self.current_rotation), rot_guess))

        position_guess = (coordinate_guess, rot_guess)
        return position_guess


    # calculate change in positino and rotation according to measured wheel rotation
    def calculate_new_position(self, wheel_position):
        # degrees that each wheel moved
        steps_left = wheel_position[0]
        steps_right = wheel_position[1]

        # moved distance / displacement
        distance = (steps_left + steps_right) * self.step_distance / 2
        # difference in rotation
        rotation_diff = (steps_right - steps_left) * self.step_distance / self.wheel_axis
        # new total rotation direction
        rotation_new = math.radians(self.current_rotation) + rotation_diff
        # test print-functions
        #print("rot. old:{}, diff:{}, new:{}".format(self.current_rotation, int(math.degrees(rotation_diff)), int(math.degrees(rotation_new))))
        #print("cos_x: {}, sin_x: {}".format(distance * math.cos(rotation_new), distance * math.sin(rotation_new)))
        # new x,y coordinates
        pos_x = self.current_position[0] + distance * math.cos(rotation_new)
        pos_y = self.current_position[1] + distance * math.sin(rotation_new)

        position_new = (pos_x, pos_y)
        rotation_new_degree = self.limit_rotation_degree(math.degrees(rotation_new))
        pos_rot_value = (position_new, rotation_new_degree)

        self.current_rotation = rotation_new_degree
        self.current_position = position_new
        #print("rotation_new: {}, position_new: {}, self_rotation: {}, self_position: {}".format(rotation_new, position_new, self.current_rotation, self.current_position))
        return pos_rot_value




