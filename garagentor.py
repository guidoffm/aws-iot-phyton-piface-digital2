#!/usr/bin/env python

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt
import pifacedigitalio
import json
from pprint import pprint

pifacedigital = pifacedigitalio.PiFaceDigital()

# Read in command-line parameters
useWebsocket = False

host = "a3mlie25r4i811.iot.eu-west-1.amazonaws.com"
rootCAPath = "root-CA.crt"
certificatePath = "garagentor.cert.pem"
privateKeyPath = "garagentor.private.key"
send_topic = "garage/inputs"
receive_topic = "garage/outputs"

missingConfiguration = False
if not useWebsocket:
	if not certificatePath:
		print("Missing '-c' or '--cert'")
		missingConfiguration = True
	if not privateKeyPath:
		print("Missing '-k' or '--key'")
		missingConfiguration = True
if missingConfiguration:
	exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.ERROR)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
	myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub", useWebsocket=True)
	myAWSIoTMQTTClient.configureEndpoint(host, 443)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
	myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub")
	myAWSIoTMQTTClient.configureEndpoint(host, 8883)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Custom MQTT message callback
def customCallback(client, userdata, message):
	x = json.loads (message.payload)
	if x["isSet"]:
		pifacedigital.output_pins[x["pin"]].turn_on()
	else:
		pifacedigital.output_pins[x["pin"]].turn_off()

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(receive_topic, 1, customCallback)
time.sleep(2)

def switch_pressed(event):
    myAWSIoTMQTTClient.publish(send_topic, json.dumps({ "pin": event.pin_num, "isSet": True }), 1)

def switch_unpressed(event):
    myAWSIoTMQTTClient.publish(send_topic, json.dumps({ "pin": event.pin_num, "isSet": False }), 1)

if __name__ == "__main__":

    listener = pifacedigitalio.InputEventListener(chip=pifacedigital)
    for i in range(4):
        listener.register(i, pifacedigitalio.IODIR_ON, switch_pressed)
        listener.register(i, pifacedigitalio.IODIR_OFF, switch_unpressed)
    listener.activate()

