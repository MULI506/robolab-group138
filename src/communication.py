#!/usr/bin/env python3

# Suggestion: Do not import the ev3dev.ev3 module in this file
import time


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
            time.sleep(30)
            self.on_message(client, data, message)
             # decodes message and creates variable
            msg = message.payload.decode('utf-8')
                # separates message
            msg.split(" ")
                # assigns message parts variables
            ack, planet_name, int_coord = msg.split(" ")  # ACK, Name planet, initial coordinates
            int_coord.split(",")
            x, y =int_coord.split(",")
            coordinates =(int(x), int(y))
            return coordinates
             # %s makes planet_name part of message
            #takes submitted location and sets it as starting place
            current_position = int_coord
            self.client.subscribe('planet/%s', qos=1 % (planet_name))
            if time.time() > time_since_received + duration : #triggers after two seconds without new message
                    break
        client.loop_stop()
        client.disconnect()
    def node(self,xn,yn,dn,xs,ys,ds): # n-new p-previous
        self.username_password_set('138', password='')
        self.connect('robolab.info.tu-dresden.de', port=8883)
        client.loop_start()
        while True :
                target_list = []
                path_list = []
                combined_list = []

                cur_pos = [str(xn), str(yn), dn]
                prev_pos = [str(xs), str(ys), ds]
                c_p = ','.join(cur_pos)
                p_p = ','.join(prev_pos)
        #checks status of path
                if cur_pos == prev_pos:
                    self.send_message('planet/%s' % (planet_name), "SYN path ,%s , %s,  blocked" % (p_p, c_p))
                    time.sleep(10)
                else:
                    self.send_message('planet/%s' % (planet_name), "SYN path, %s, %s free" % (p_p, c_p))
                    coordinate_list.append(cur_pos)
                    time.sleep(10)
            self.on_message(client, data, message)
            if time.time() > time_since_received + duration:
                break
            node_msg = message.payload.decode('utf-8')
            if len(nod_msg) < 20 : #there probably is a more elegant solution to this
                node_msg.split(" ")
                ack, trigger, received_target = node_msg.split(" ")
                xt, yt = received_target.split(",")
                target = (int(xt), int(yt))
                target_list.append(target)
                combined_list.append(target_list)

            else :
                a,pa,new_coord1,new_coord2,stat,weight = node_msg.split(" ") #rename variables later # ACK Path  (x,y,d) (x,y,d) free/blocked weight
                xr,yr,dr = new_coord1.split(",")
                xnn,ynn,dnn = new_coord2.split(",") #again, renaming them later
                # covers first message with corrected coordinates
                if  prev_pos == new_coord1:
                        cur_pos = new_coord2
                #all received paths into list
                received_path = (int(xr), int(yr), dr, int(xnn),int(ynn),dnn, int(weight))
                path_list.append(received_path)
                combined_list.append(path_list)


    #if target = current_position
    def target_reached(self): #incomplete
        self.username_password_set('138', password='')
        self.connect('robolab.info.tu-dresden.de', port=8883)
        client.loop_start()
        while True :
            self.send_message('explorer/138' "SYN target reached")
            send_time = time.time()
            if time.time() > send_time + 2 :
                break
        client.loop_stop()
        client.disconnect()
    #no paths left
    def explore_com(self):
        self.username_password_set('138', password='')
        self.connect('robolab.info.tu-dresden.de', port=8883)
        self.subscribe('explorer/138', qos=1)
        client.loop_start()
        while True :
            self.send_message('explorer/138' "SYN exploration completed!")
            send_time = time.time()
            if time.time() > send_time + 2 :
                break
        client.loop_stop()
        client.disconnect()


