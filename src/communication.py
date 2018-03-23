#!/usr/bin/env python3

# Suggestion: Do not import the ev3dev.ev3 module in this file
import time

import self as self


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
        print('message with topic "{}"'.format(message.topic))
        print('message was "{}"'.format(message.payload.decode('utf-8')))
        """ Handles the callback if any message arrived """
        time_since_received = time.time() #everytime message is received timer resets
        duration = 2
        pass

    # Example
    def send_message(self, topic, message):
        """ Sends given message to specified channel """
        self.client.publish.single(topic, message, 1, False)
        pass

    def landing(self):
        self.username_password_set('138', password='')  # don't know what pass has to be   #whole thing might be wrong here
        self.connect('robolab.info.tu-dresden.de', port=8883)  # server used to communicate
        self.subscribe('explorer/138', qos=1)  # qos1-> message arrives at least once
        client.loop_start()
        while True :
            self.send_message('explorer/138', "SYN ready")
            time.sleep(10)
            self.on_message(client, data, message)
             # decodes message and creates variable
            msg = message.payload
                # separates message
            msg.split(" ")
                # assigns message parts variables
            ack, planet_name, int_coord = msg.split(" ")  # ACK, Name planet, initial coordinates
            int_coord.split(",")
            x, y =int_coord.split(",")
            coordinates =(int(x), int(y))


             # %s makes planet_name part of message
            self.client.subscribe('planet/%s', qos=1) % planet_name
            #takes submitted location and sets it as starting place
            current_position = int_coord
            if time.time() > time_since_received + duration : #triggers after two seconds without new message
                    break
        client.loop_stop()
        client.disconnect()
        #need to set up lists still
    def node(self):
        self.username_password_set('138', password='')
        self.connect('robolab.info.tu-dresden.de', port=8883)
        self.subscribe('planet/%s', qos=1) % planet_name #already subbed to topic so line shouldn't be needed
        client.loop_start()
        while True :
        #checks status of path
                if current_position = previous_position
                    self.send_message('planet/%s', "SYN path,previous_position,current_position,De blocked") % planet_name
                    time.sleep(10)
                else:
                    self.send_message('planet/%s', "SYN path,previous_position,Ds,current_position,De free") % planet_name
                    coordinate_list.append(current_position)
                    time.sleep(10)
            self.on_message(client, data, message)
            if time.time() > time_since_received + duration:
                break
            node_msg = message.payload
            if len(nod_msg) < 20 #there probably is a more elegant solution to this
                node_msg.split(" ")
                ack, trigger, target = node_msg.split(" ")
                    if path_to_target in path_list #<-- not a thing yet
                        '''move to target'''
                    else '''save target'''
            else:
                a,pa,target,new_coord1,new_coord2,stat,wei = node_msg.split(" ") #rename variables later # ACK Path target (x,y,d) (x,y,d) free/blocked weight
                xn,yn,d = new_coord1.split(",")
                xnn,ynn,dn = new_coord2.split(",") #again, renaming them later
                received_path = (int(xn), int(yn), d, int(xnn),int(ynn),dn)
                add_path #the received one


    #if target = current_position
    def target_reached(self): #incomplete
        self.username_password_set('138', password='')
        self.connect('robolab.info.tu-dresden.de', port=8883)
        self.subscribe('explorer/138', qos=1)
        client.loop_start()
            self.send_message('explorer/138' "SYN target reached")
        client.loop_stop()
        client.disconnect()
    #no paths left
    def explore_com(self):
        self.username_password_set('138', password='')
        self.connect('robolab.info.tu-dresden.de', port=8883)
        self.subscribe('planet/%s', qos=1)
        client.loop_start()
            self.send_message('explorer/138' "SYN exploration completed!")
        client.loop_stop()
        client.disconnect()


