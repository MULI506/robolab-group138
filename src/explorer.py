from driver import *
from planet import *
#from communication import *
import time


"""
PROJECT STRUCTURE:
Main-Control: explorer
explorer <-> communication
explorer <-> driver
explorer <-> planet

driver <-> odometry
driver -> motor
driver <- colorsensor
driver <- ursensor

driver <- sounds
"""""


class Explorer:

    def __init__(self):
        self.drive = Driver()
        self.planet = Planet()

        self.position_known = (0, 0)
        self.direction_known = 0

    # complete exploration_process
    def explore_offline(self):
        self.start_exploration(False)
        self.follow_path_add()
        self.show_all_paths()

    # enters planet and sets initial coordinate
    def start_exploration(self, online):
        self.drive.follow_line_complete((0, 0), 0)
        # sets first position
        # if online-mode, connect to server and get first position, otherwise set to (0,0)
        if online:
            """"
            # COMMUNICATE WITH SERVER AND GET COORDINATE
            self.position_known = (x, y)
            """
            pass
        else:
            self.position_known = (0, 0)
        # starting direction is NORTH
        self.direction_known = 0
        # adds first coordinate to structure
        self.planet.add_new_coordinate(self.position_known)

        # detects lines at coordinate
        line_result = self.drive.detect_lines(self.direction_known)
        # gets the current rotation value and resets it to the guessed direction
        new_rotation = line_result[0]
        self.direction_known = self.quantize_direction(new_rotation)
        # detected lines as List [North, West, South, East]
        detected_lines = line_result[1]
        # ignores the entry path to the planet, sets found path in South to False
        detected_lines[2] = False

        print("Starting Position: {}, Current Rotation: {}".format(self.position_known, self.direction_known))

    #
    def follow_path_add(self):
        new_position = self.drive.follow_line_complete(self.position_known, self.direction_known)
        print(new_position)
        time.sleep(1)

        new_coordinate = new_position[0]
        new_direction = self.quantize_direction(new_position[1])

        self.planet.add_new_coordinate(new_coordinate)
        self.planet.add_path((self.position_known, self.convert_direction(self.direction_known)),
                             (new_coordinate, self.convert_direction(new_direction)), 1)

    # prints all saved paths
    def show_all_paths(self):
        self.planet.print_paths()

    #def turn_to_direction(self, direction):
    #    pass


    # resets the direction according to the current rotation value
    def quantize_direction(self, rotation):
        # NORTH
        if 0 <= rotation < 45 or rotation >= 315:
            return 0
        # WEST
        elif 45 <= rotation < 135:
            return 90
        # SOUTH
        elif 135 <= rotation < 225:
            return 180
        # EAST
        elif 225 <= rotation < 315:
            return 270
        # ERROR
        else:
            return -1

    # resets the direction according to the current rotation value
    def convert_direction(self, rotation):
        # NORTH
        if rotation == 0:
            return Direction.NORTH
        elif rotation == 90:
            return Direction.WEST
        elif rotation == 180:
            return Direction.SOUTH
        elif rotation == 270:
            return Direction.EAST
        else:
            return 'ERROR'


    def test_paths(self):
        self.planet.add_path(((0, 0), Direction.NORTH), ((1, 1), Direction.SOUTH), 1)
        self.planet.add_path(((2, 3), Direction.WEST), ((1, 1), Direction.NORTH), 2)
        self.planet.add_path(((2, 3), Direction.SOUTH), ((0, 0), Direction.WEST), 3)
        self.planet.print_paths()
        print("############")
        self.planet.get_paths()


