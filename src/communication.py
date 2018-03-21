#!/usr/bin/env python3

# Suggestion: Do not import the ev3dev.ev3 module in this file


class Communication:
    """
        Class to hold the MQTT client

        Feel free to add functions, change the constructor and the example send_message() to satisfy your requirements and thereby solve the task according to the specifications
    """

    def __init__(self, mqtt_client):
        """ Initializes communication module, connect to server, subscribe, etc. """
        # THESE TWO VARIABLES MUST NOT BE CHANGED
        self.client = mqtt_client
        self.client.on_message = self.on_message

        # ADD YOUR VARIABLES HERE

    # THIS FUNCTIONS SIGNATURE MUST NOT BE CHANGED
    def on_message(self, client, data, message):
        print('message with topic ""'.format(message.topic))
        print('message was ""'.format(message.payload.decode('utf-8')))
        """ Handles the callback if any message arrived """
        pass

    # Example
    def send_message(self, topic, message):
        """ Sends given message to specified channel """
        self.client.publish(topic, message, 1, False)
        pass

    def landing(self):
        self.username_password_set('138', password='')  # dont know what pass has to be   #whole thing might be wrong here
        self.connect('robolab.info.tu-dresden.de', port=8883)  # server used to communicate
        self.subscribe('explorer/138', qos=1)  # qos1-> message arrives at least once

        send_message('explorer/138', "SYN ready")
        self.on_message
        # decodes message and creates variable
            msg = message.payload
            # seperates message
            msg.split(" ")
            # assigins message parts variables
        ack, planet, int_coord = msg.split(" ")  # ACK, Name planet, initial coordinates
        coordinate_list = [int_coord]

        assert isinstance(planet, object)
        self.subscribe(planet, qos=1)
        #takes submitted location and sets it as starting place
        current_position = int_coord
        #need to set up lists still
    def node(self, current_position=None): #need to create that still
        if current_position in coordinate_list
            send_message('planet', "SYN path",current_position,current_position,De "blocked")
        else:
            send_message('planet', "SYN path",previous_position,,Ds,current_position,De "free")
            coordinate_list.append(current_position)
        self.on_message
            add_path #function in planet.py, not set up yet #might not be needed here
                node_msg = message.payload
                node_msg.split(" ")
                a,target,c = node_msg.split(" ") #rename variables later
                if target == "target" and c in path_list #<-- not a thing yet
                    '''move to c''' #need to figure out how
                else '''save c'''   #^

