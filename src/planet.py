#!/usr/bin/env python3

from enum import IntEnum, unique
from typing import List, Optional, Tuple, Dict
# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE


@unique
class Direction(IntEnum):
    """ Directions in degrees """
    NORTH = 0
    EAST  = 90
    SOUTH = 180
    WEST  = 270


# simple alias, no magic here
Weight = int
""" 
    Weight of a given path (received from the server)
    value:  -1 if broken path 
            >0 for all other paths
            never 0
"""


class Planet:
    """ 
    Contains the representation of the map and provides certain functions to manipulate it according to the specifications 
    """

    def __init__(self):
        """ Initializes the data structure """
        self.target = None

        # data for paths
        self.path_data = {}
        # data for paths, that can still be explored
        self.open_paths = {}

    def add_path(self, start: Tuple[Tuple[int, int], Direction], target: Tuple[Tuple[int, int], Direction], weight: int):
        """ 
        Adds a bidirectional path defined between the start and end coordinates to the map and assigns the weight to it 

        example: 
            add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 1)

        current path structure:
            path_data{(coordinate):[[path1][path2][path3]], (coordinate):[[path1][path2]], ...}
            path = [start_position, start_direction, end_position, end_direction, weight]
        """
        start_position = start[0]
        start_direction = start[1]
        end_position = target[0]
        end_direction = target[1]

        # checks, if coordinate exists in data structure and adds it
        if not self.check_coordinate_known(end_position):
            self.add_new_coordinate(end_position)
        if not self.check_coordinate_known(start_position):
            self.add_new_coordinate(start_position)

        # checks, if current path is saved and adds it
        if not self.check_path_known(start_position, start_direction):
            # adds path from start to end
            self.path_data[start_position].append([start_position, start_direction, end_position, end_direction, weight])
            # adds path from end to start
            self.path_data[end_position].append([end_position, end_direction, start_position, start_direction, weight])


    def get_paths(self) -> Dict[Tuple[int, int], Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]]:
        """ 
        Returns all paths 

        example: 
            get_paths() returns: { 
                                    (0, 3): {
                                                Direction.NORTH: ((0, 3), Direction.WEST, 1), 
                                                Direction.EAST: ((1, 3), Direction.WEST, 2) 
                                            },
                                    (1, 3): {
                                                Direction.WEST: ((0, 3), Direction.EAST, 2), 
                                                ... 
                                            }, 
                                    ...
                                  }
        """
        # initializes empty dictionary
        path_result = {}
        # goes through every coordinate in path structure
        for coordinate in self.path_data.keys():
            # creates a dictionary for every coordinate
            path_result[coordinate] = {}
            # for every path for each coordinate
            for single_path in self.path_data.get(coordinate):
                # creates key-value pairs for each path according to given return structure
                path_result[coordinate][single_path[1]] = (single_path[2], single_path[3], single_path[4])
        print(path_result)
        # returns all paths according to given structure
        return path_result



    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Optional[List[Tuple[Tuple[int, int], Direction]]]:
        """ 
        Returns a shortest path between two nodes 

        examples: 
            shortest_path((0,0), (2,2)) returns: [((0, 0), Direction.EAST), ((1, 0), Direction.NORTH)]
            shortest_path((0,0), (1,2)) returns: None
        """
        pass

    # adds a new coordinate to the path data
    def add_new_coordinate(self, new_coordinate: Tuple[int, int]):
        # set coordinate as new key and create as value an empty list for each path
        self.path_data[new_coordinate] = []

    # checks, if a coordinate exists in the path data
    def check_coordinate_known(self, new_coordinate: Tuple[int, int]):
        for coord in self.path_data.keys():
            if coord == new_coordinate:
                return True
        return False

    # checks, if a path exists in the path data
    def check_path_known(self, start_pos: Tuple[int, int], start_dir: int):
        paths_from_position = list(self.path_data.get(start_pos))
        for path in paths_from_position:
            if path[1] == start_dir:
                return True
        return False

    # if coordinate isn't part of detected-path-data, then add it
    def add_detected_paths(self, coordinate, detected_paths):
        if coordinate in list(self.open_paths.keys()):
                return
        self.open_paths[coordinate] = detected_paths

    # returns data of all directions per node, left to explore
    def get_open_paths(self):
        return self.open_paths

    # returns data for all saved paths
    def get_path_data(self):
        return self.path_data

    # sets a direction at a coordinate to false, which marks it as explored
    def close_open_path(self, coordinate, direction):
        # sets correct index value for the current direction
        if direction == 0:
            index = 0
        elif direction == 90:
            index = 1
        elif direction == 180:
            index = 2
        else:
            index = 3
        # sets the boolean value for the direction to False
        self.open_paths[coordinate][index] = False

    # print out all paths
    def print_paths(self):
        print("PATHS")
        for coordinate in self.path_data.keys():
            print("{}:".format(coordinate))
            for path in self.path_data.get(coordinate):
                dir = path[1]
                if dir == 0:
                    dir = 'NORTH'
                elif dir == 90:
                    dir = 'EAST'
                elif dir == 180:
                    dir = 'SOUTH'
                else:
                    dir = 'WEST'
                dir_end = path[3]
                if dir_end == 0:
                    dir_end = 'NORTH'
                elif dir_end == 90:
                    dir_end = 'EAST'
                elif dir_end == 180:
                    dir_end = 'SOUTH'
                else:
                    dir_end = 'WEST'
                print("    Start:{}, {} | End:{}, {} | Weight: {}".format(path[0], dir, path[2], dir_end, path[4]))

    # test Direction class
    def direction_test(self, direc: Direction):
        print(direc)
