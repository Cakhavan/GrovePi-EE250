import paho.mqtt.client as mqtt
import time
import grovepi 
from grovepi import *
import math
from grove_rgb_lcd import *


# MQTT variables and topics
broker_hostname = "eclipse.usc.edu"
broker_port = 11000
led_topic = "anrg-pi12/led"
lcd_topic= "anrg-pi12/lcd"
humidity_topic = "anrg-pi12/humidity"
temp_topic = "anrg-pi12/temperature" 

#set up GrovePi temp/hum sensor
sensor = 7 
blue = 0    # The Blue colored sensor.
white = 1   # The White colored sensor.

#initialize and set variables
led = "0"
temperature = 0
hum = 0
lcd = ""

#set Pin as output for led
pinMode(5,"OUTPUT")

#Set lcd screen
setRGB(0,255,0)



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    #subscribe to topics
    client.subscribe(led_topic)
    client.subscribe(lcd_topic)

    #create callbacks
    client.message_callback_add(led_topic, led_callback)
    client.message_callback_add(lcd_topic,lcd_callback)



def led_callback(client, userdata, msg):
    global led
    
    #toggle the led variable when a message is received
    if led == "1" and str(msg.payload,"utf-8") == "1":
        
        #turn off led
        digitalWrite(5,0)
        #toggle back variable to 0
        led=  "0"

    else: 
        #turn on led
        digitalWrite(5,1)
        led = str(msg.payload, "utf-8")


    #print led status to terminal for testing
    print("on_message: " + msg.topic + " " + led)
    if led == "0":
            print("LED IS OFF")
    else:
            print("LED IS ON")


def lcd_callback(client, userdata, msg):
    global lcd
    #convert msg to utf-8 string
    lcd = str(msg.payload, "utf-8")
    #print to screen 
    setText(lcd)
    #print to terminal for testing
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


if __name__ == '__main__':
    # Connect to broker and start loop    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host = broker_hostname, port = broker_port, keepalive =  60)
    client.loop_start()

    
 
    global blue
    while True:

        #gather temp,hum data from sensor
        [temp,humidity] = grovepi.dht(sensor, blue) 
        #print data to terminal for testing
        print("Temp: " + str(temp) + "\n")
        print("Humidity: " + str(humidity) + "\n")
        #publish hum/temp to respective topics   
        client.publish(humidity_topic, humidity)
        client.publish(temp_topic, temp)
            
       
        
        time.sleep(0.2)