#!/usr/bin/env python

import paho.mqtt.client as mqtt
import os
from urllib.parse import urljoin

open_comms = []
p_mqttc = None
p_uname = None
# Define event callbacks
def on_connect(client, userdata, flags, rc):
    return
    #print("rc: " + str(rc))

def on_message(client, obj, msg):
    global p_uname
    global open_comms
    #print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    pl = str(msg.payload)
    sender = pl[pl.index('<')+1:pl.index('>')]
    code = pl[pl.index('[')+1:pl.index(']')]
    if code == '100':
        client.publish(sender, "Sender<" + p_uname + "> CODE[101]")
    if code == '101':
        print(sender + " is online.")

def on_publish(client, obj, mid):
    #print("mid: " + str(mid))
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

# Start subscribe, with QoS level 0
    mqttc.subscribe(uname, 0)

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