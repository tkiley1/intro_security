#!/usr/bin/env python

import paho.mqtt.client as mqtt
import os
from urllib.parse import urljoin

open_comms = []
p_mqttc = None
p_uname = None
# Define event callbacks
def on_connect(client, userdata, flags, rc):
    global loop_flag
    logging.info("Connected flags" + str(flags) + "result code " + str(rc) + "for client.")
    client.connected_flag = True
    loop_flag = 0
    #return
    #print("rc: " + str(rc))

def on_message(client, obj, msg):
    global open_comms
    payload = msg.payload
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    try:
        if len(payload) == 150: # payload is a message instead of a file
            message_handler(msg, client)
        else:
            print("Recieving file...")
            file_handler(msg)
            print(" Done!")
    except Exception as e:
        print("Encoutered exception in message: ")
        print(e)

def file_handler(msg):
    payload = msg.payload
    file_name = payload[0:payload.index(b'\0')]
    print("File")
    if b'/' == file_name[0] or b'..' in file_name:
        print("Dangerous pathing detected, rejecting file!")
    else:
        file_buff = payload[payload.index(b'\0')+2:]
        f_out = open(file_name, 'wb')
        f_out.write(file_buff)

def message_handler(msg, client):
    global p_uname
    pl = str(msg.payload)
    sender = pl[pl.index('<')+1:pl.index('>')]
    code = pl[pl.index('[')+1:pl.index(']')]
    print(code)
    if code == '100':
        # print(sender + " is online.")
        message = "Sender<" + p_uname + "> CODE[101]"
        print(message)
        message += '\0'*(150-len(message))
        message = bytearray(message, 'UTF-8')
        client.publish(sender, message) #"Sender<" + p_uname + "> CODE[101]")
    elif code == '101':
        print(sender + " is online.")
    elif code == '200':
        pass # TODO: file metadata header


def on_publish(client, obj, mid):
    print("mid: " + str(mid))
    return

def on_subscribe(client, obj, mid, granted_qos):
    #print("Subscribed: " + str(mid) + " " + str(granted_qos))
    return

def on_log(client, obj, level, string):
    #print(string)
    return
def initialize(uname):
    global p_uname
    mqttc = mqtt.Client()
    p_uname = uname
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
#mqttc.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)
#url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
#url = urljoin(url_str)
#topic = url.path[1:] or 'test'
    url = "m15.cloudmqtt.com"
# Connect
    mqttc.username_pw_set('oxpjhofa', "0DdqvNd75j9n")
    mqttc.connect(url, 16523)

# Start subscribe, with QoS level 1
    mqttc.subscribe(uname, 1)

# Publish a message
    #mqttc.publish("0", "FOO")

# Continue the network loop, exit when an error occurs
    return mqttc
def listen(mqttc):
    for i in range(3):
        rc = 0
        #mqttc.publish("0", "Stuff")
        rc = mqttc.loop()
        #print("rc: " + str(rc))

def publish(mqttc, topic, content):
        #print("Publishing topic: " + str(topic) + " Content: " + str(content))
        mqttc.publish(topic, content)
        return 0

#listen()
