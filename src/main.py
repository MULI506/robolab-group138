#!/usr/bin/env python3

import uuid
import paho.mqtt.client as mqtt

from explorer import *
from driver import *
from sensors.colorsensor import *
from sounds import *
#from communication import *

client = None # DO NOT EDIT


def run():
    # DO NOT EDIT
    global client
    client = mqtt.Client(client_id=str(uuid.uuid4()),  # client_id has to be unique among ALL users
                         clean_session=False,
                         protocol=mqtt.MQTTv31)

    # the execution of all code shall be started from within this function
    # ADD YOUR OWN IMPLEMENTATION HEREAFTER
    print("Hello World!")

    # main control class/object for exploration
    exp = Explorer()
    # start whole exploration process without communication
    exp.explore_offline()
    # print all detected paths
    exp.show_all_paths()



# DO NOT EDIT
if __name__ == '__main__':
    run()