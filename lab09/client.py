import paho.mqtt.client as mqtt
import time
import grovepi 
from grovepi import *
import math
from grove_rgb_lcd import *


# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000
led_topic = "anrg-pi12/led"
lcd_topic= "anrg-pi12/lcd"
humidity_topic = "anrg-pi12/humidity"
temp_topic = "anrg-pi12/temperature" 

sensor = 4 
blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.

led = "0"
temperature = 0
hum = 0
lcd = ""


setRGB(0,255,0)

setText("hello")



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(led_topic)
    client.subscribe(lcd_topic)
    client.message_callback_add(led_topic, led_callback)
    client.message_callback_add(lcd_topic,lcd_callback)

def led_callback(client, userdata, msg):
    global led
    
    if led == "1" and str(msg.payload,"utf-8") == "1":
        digitalWrite(4,0)
        led=  "0"

    else: 
        digitalWrite(4,1)
        led = str(msg.payload, "utf-8")

    print("on_message: " + msg.topic + " " + led)
    if led == "0":
            print("LED IS OFF")
    else:
            print("LED IS ON")


def lcd_callback(client, userdata, msg):
    global lcd
    lcd = str(msg.payload, "utf-8")
    setText(lcd)
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def humidity_callback(client, userdata, msg):
    global humidity
    hum = int(msg.payload, "utf-8")
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def temp_callback(client, userdata, msg):
    global temperature
    temperature = int(msg.payload, "utf-8")
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


def on_message(client, userdata, msg): 
    print(msg.topic + " " + str(msg.payload))


if __name__ == '__main__':
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host = broker_hostname, port = broker_port, keepalive =  60)
    client.loop_start()

 

    while True:

        if led == "0":
            print("LED IS OFF")
        else:
            print("LED IS ON")

        [temp,humidity] = grovepi.dht(sensor,blue) 

        if math.isnan(temp) == False and math.isnan(humidity) == False:

            client.publish(humidity_topic, humidity)
            client.publish(temp_topic, temp)
            
       
        
        time.sleep(0.2)