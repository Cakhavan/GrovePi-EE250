import paho.mqtt.client as mqtt
import time


# MQTT variables
broker_hostname = "eclipse.usc.edu"
broker_port = 11000
led_topic = "anrg-pi12/led"
lcd_topic= "anrg-pi12/lcd"
humidity_topic = "anrg-pi12/humidity"
temp_topic = "anrg-pi12/temperature" 

ranger1_dist = 5

def led_callback(client, userdata, msg):
    global ranger1_dist
    
    #truncate list to only have the last MAX_LIST_LENGTH values
    ranger1_dist = int(msg.payload)

#def ranger2_callback(client, userdata, msg):
#    global ranger2_dist
 #   ranger2_dist.append(min(125, int(msg.payload)))
    #truncate list to only have the last MAX_LIST_LENGTH values
  #  ranger2_dist = ranger2_dist[-MAX_LIST_LENGTH:]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(led_topic)
    client.message_callback_add(led_topic, led_callback)
  #  client.subscribe(ultrasonic_ranger2_topic)
   # client.message_callback_add(ultrasonic_ranger2_topic, ranger2_callback)

# The callback for when a PUBLISH message is received from the server.
# This should not be called.
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
  
        
        print("data " + str(ranger1_dist) )

       
        
        time.sleep(0.2)