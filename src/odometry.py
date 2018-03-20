# Suggestion: 	implement odometry as class that is not using the ev3dev.ev3 package
# 				establish value exchange with main driving class via getters and setters

from typing import List, Optional, Tuple, Dict
import math

class Odometry():

    def __init__(self):
        # setup values for position and rotation
        self.current_position = (0, 0)
        self.current_rotation = 0

        # setup wheel diameter and wheel separation
        self.wheel_dia = 55
        self.wheel_axis = 110  #measured middle: 120mm
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

    # keep the rotation between 0 and 360 degrees
    def limit_rotation_degree(self, rot_deg):
        return rot_deg % 360

    # calculate change in positino and rotation according to measured wheel rotation
    def calculate_new_position(self, wheel_position, position_robot_old, rotation_old, axis):
        # degrees that each wheel moved
        steps_left = wheel_position[0]
        steps_right = wheel_position[1]

        # moved distance / displacement
        distance = (steps_left + steps_right) * self.step_distance / 2
        # difference in rotation
        rotation_diff = (steps_right - steps_left) * self.step_distance / axis
        # new total rotation direction
        rotation_new = rotation_old + rotation_diff
        # test print-functions
        #print("rot. old:{}, diff:{}, new:{}".format(int(math.degrees(rotation_old)), int(math.degrees(rotation_diff)), int(math.degrees(rotation_new))))
        #print("cos_x: {}, sin_x: {}".format(distance * math.cos(rotation_new), distance * math.sin(rotation_new)))
        # new x,y coordinates
        pos_x = position_robot_old[0] + distance * math.cos(rotation_new)
        pos_y = position_robot_old[1] + distance * math.sin(rotation_new)

        position_new = (pos_x, pos_y)
        pos_rot_value = (position_new, self.limit_rotation_degree(math.degrees(rotation_new)))
        return pos_rot_value




