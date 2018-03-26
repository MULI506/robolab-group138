from driver import *
from planet import *
from sounds import *
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
        self.sounds = Sounds()

        self.position_known = (0, 0)
        self.direction_known = 0

    # complete exploration_process
    def explore_offline(self):
        # start exploration, drive to first node
        self.start_exploration(False)
        while True:
            # check, if current node has unexplored paths
            node_status = self.check_node_paths(self.position_known)
            # if all paths are explored
            if node_status == 'explored':
                # a list of paths to a node with unexplored paths (BFS)
                path_to_explore = self.search_unexplored_node()
                # if no node has unexplored paths, the whole planet is explored
                if path_to_explore == 'finished':
                    # shows
                    self.sounds.victory()
                    return
                # move to the node with unexplored paths
                self.follow_path_to_target(path_to_explore)
                continue
            # if current node has unexplored paths, turn to that direction, follow the path and scan the new node
            else:
                self.turn_to_direction(node_status)
                self.follow_path_add()
                self.scan_paths()


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
        self.planet.add_detected_paths(self.position_known, detected_lines)
        print("Starting Position: {}, Current Rotation: {}".format(self.position_known, self.direction_known))

    # follows a path from start to finish and adds the path to the path data
    def follow_path_add(self):
        # follows the line and gets the data back (end_coordinate, end_direction, path_status)
        path_result = self.drive.follow_line_complete(self.position_known, self.direction_known)
        time.sleep(1)

        new_coordinate = path_result[0]
        new_direction = self.quantize_direction(path_result[1])

        # checks path status and sets weight accordingly
        path_status = path_result[2]
        if path_status == 'free':
            # rough weight guess according to coordination change
            weight = int((math.fabs(self.position_known[0]-new_coordinate[0])+math.fabs(self.position_known[1]-new_coordinate[1])))
        else:
            weight = -1

        # calculates direction, where the robot came from
        direction_arrived = (new_direction + 180) % 360
        print("NEW: coordinate: {}, direction: {}, direction arrived: {}, path status: {}".format(new_coordinate, new_direction, direction_arrived, path_status))

        # adds the path to the data structure
        self.planet.add_path((self.position_known, self.convert_to_direction(self.direction_known)),
                             (new_coordinate, self.convert_to_direction(direction_arrived)), weight)

        # sets the driven path to explored
        self.planet.close_open_path(self.position_known, (self.direction_known))
        # set current known position and direction to new values
        self.position_known = new_coordinate
        self.direction_known = new_direction

    # scan the outgoing paths at a node, if they are not scanned yet
    def scan_paths(self):
        # get data for available paths
        open_path_data = self.planet.get_open_paths()
        arrived_from = (self.direction_known + 180) % 360
        # check if coordinate is already saved
        if self.position_known not in list(open_path_data.keys()):

            # if it's not saved, scan the node for paths
            scan_data = self.drive.detect_lines(self.direction_known)
            # set current direction to the final direction after scan
            self.direction_known = self.quantize_direction(scan_data[0])
            # gets data for scanned paths
            detected_paths = scan_data[1]
            # adds scanned paths to data structure
            self.planet.add_detected_paths(self.position_known, detected_paths)
        self.planet.close_open_path(self.position_known, arrived_from)

        print("coord: {}, adjusted: {}".format(self.position_known,
                                                             self.planet.get_open_paths().get(self.position_known)))

    # checks, if there is an unexplored path at the current position
    def check_node_paths(self, position):
        # list of unexplored outgoing paths for this node
        current_node = self.planet.get_open_paths().get(position)
        # if a path is unexplored, return the direction
        if True in current_node:
            direction_index = current_node.index(True)
            # NORTH
            if direction_index == 0:
                return 0
            # WEST
            elif direction_index == 1:
                return 90
            # SOUTH
            elif direction_index == 2:
                return 180
            # EAST
            elif direction_index == 3:
                return 270
        # if there is no unexplored path
        else:
            return 'explored'

    # looks for node with unexplored paths and returns the path to the node
    # return format: List[((x1,y1, direction1), ((x2,y2), direction2), ((x3,y3, direction3), ...]
    # Breadth First Search
    def search_unexplored_node(self):
        # currently saved path data
        path_data = self.planet.get_path_data()
        # list of coordinates to be used
        coordinate_queue = []
        # list of coordinates already used
        used_coordinates = []
        # link between coordinates, used to create the path between nodes in the end
        coordinate_links = []
        # add the current position
        coordinate_queue.append(self.position_known)
        used_coordinates.append(self.position_known)
        while True:
            # if no coordinate is
            if not coordinate_queue:
                return 'finished'
            # take the first coordinate of the list
            coordinate = coordinate_queue.pop(0)
            # get all paths from that coordinate
            outgoing_paths = path_data.get(coordinate)
            # for every outgoing path
            for path in outgoing_paths:
                # if the end of the path (coordinate) hasn't been used yet
                if path[2] not in used_coordinates:
                    # add the coordinate
                    coordinate_queue.append(path[2])
                    used_coordinates.append(path[2])
                    # add a link between the current and next coordinate using coordinates and directions
                    coordinate_links.append([path[0], self.convert_from_direction(path[1]),
                                            path[2], self.convert_from_direction(path[3])])
                    # if a node with unexplored paths is found
                    if self.check_node_paths(path[2]) is not 'explored':
                        # use that path as target
                        found = path[2]
                        target = path[2]
                        # create empty list for the paths from start to finish
                        path_result = []
                        # create the whole path list
                        while True:
                            # check the coordinate links for the current target
                            for link in coordinate_links:
                                # if the target is found as link-target
                                if link[2] == target:
                                    # the link-start coordinate and direction are added in front of the whole path list
                                    path_result.insert(0, (link[0], link[1]))
                                    # set the added coordinate as new target
                                    target = link[0]
                                    # if target has reached the current position, the list is complete
                                    if target == self.position_known:
                                        print("from:{} to:{} path:{}".format(self.position_known, found, path_result))
                                        # return the list
                                        return path_result
                                    break
            #print("queue: {}, outgoing_paths: {}".format(coordinate_queue, outgoing_paths))
            #print("coord links: {}".format(coordinate_links))

    # follow a path to a target coordinate
    def follow_path_to_target(self, path):
        # given path
        path_to = path
        print(path_to)
        while True:
            # take the first path value and remove it from the path-list (coordinate, direction)
            go_to = path_to.pop(0)
            # get the direction from the current coordinate
            direction = go_to[1]
            print("goto: {}, direction: {}".format(go_to, direction))
            # turn to that direction
            self.turn_to_direction(direction)
            # follow the current path
            self.follow_path_add()
            time.sleep(0.5)
            # if there is no more path to follow / target is reached: end
            if not path_to:
                break

    # prints all saved paths
    def show_all_paths(self):
        self.planet.print_paths()

    # show all data for available paths for each node
    def show_all_detected(self):
        print(self.planet.get_open_paths())

    # turns to a given direction according to starting direction
    def turn_to_direction(self, new_direction):
        old_direction = self.direction_known
        # how far to turn
        degrees = (new_direction - old_direction) % 360
        # turn that far
        self.drive.turn_by_degree(degrees)
        self.drive.hug_line()
        self.direction_known = int(new_direction)
        print("New direction is: {}".format(self.direction_known))

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

    # returns the index for the given direction
    def direction_index(self, direction):
        # NORTH
        if direction == 0:
            return 0
        # WEST
        elif direction == 90:
            return 1
        # SOUTH
        elif direction == 180:
            return 2
        # EAST
        elif direction == 270:
            return 3
        else:
            return -1

    # converts the direction to the preset IntEnum values
    def convert_to_direction(self, rotation):
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

    # converts the direction from the preset IntEnum values
    def convert_from_direction(self, direction):
        if direction == Direction.NORTH:
            return 0
        elif direction == Direction.WEST:
            return 90
        elif direction == Direction.SOUTH:
            return 180
        elif direction == Direction.EAST:
            return 270
        else:
            return 'ERROR'

    # test function for path saving and output
    def test_paths(self):
        self.planet.add_path(((0, 0), Direction.NORTH), ((1, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 0), Direction.NORTH), ((1, 1), Direction.SOUTH), 1)
        self.planet.add_path(((2, 3), Direction.WEST), ((1, 1), Direction.NORTH), 2)
        self.planet.add_path(((2, 3), Direction.SOUTH), ((0, 0), Direction.WEST), 3)
        self.planet.add_path(((5, 6), Direction.WEST), ((7, 7), Direction.EAST), 4)
        self.planet.add_path(((7, 7), Direction.EAST), ((5, 6), Direction.WEST), 4)
        self.planet.print_paths()
        print("############")
        self.planet.get_paths()

