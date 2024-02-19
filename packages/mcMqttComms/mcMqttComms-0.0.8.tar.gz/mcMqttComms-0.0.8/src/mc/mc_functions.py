# Mission control communication functionality

import paho.mqtt.client as mqtt
import base64
import json
import boto3




def publishMessage(topic, message, user, pw, ec2ipv4):
    client = mqtt.Client()
    client.username_pw_set(username=user, password=pw)
    client.on_message = on_message
    client.connect(ec2ipv4, 1883, 60)
    client.on_publish = on_publish

    client.publish(topic, message, 2)
    client.loop_forever()





def subscribeToAll(user, pw, ec2ipv4):
    client = mqtt.Client()
    client.username_pw_set(username=user, password=pw)
    client.on_message = on_message
    
    # Subscribe to all topics under broker
    client.connect(ec2ipv4, 1883, 60)
    client.subscribe("#")
    client.loop_forever()


# Handler for subscribing and receiving messages
def on_message(client, userdata, msg):
    print("Message received for Topic:", msg.topic)
    # If specified topic contains topic name (any messsage under topic subtopics) then save to dedicated text file for specified topic
    if "health" in msg.topic:
        with open('messagingData/health.json', 'a+') as healthF:
            healthF.write("Message Received:" + (msg.payload).decode() + "\n")
    if "navigation" in msg.topic:
        with open('messagingData/navigation.json', 'a+') as navF:
            navF.write("Message Received:" + (msg.payload).decode() + "\n")
    if "telemetry" in msg.topic:
        with open('messagingData/telemetry.json', 'a+') as telF:
            telF.write("Message Received:" + (msg.payload).decode() + "\n")
    if "control" in msg.topic:
        with open('messagingData/control.json', 'a+') as conF:
            conF.write("Message Received:" + (msg.payload).decode() + "\n")


# Handler for publishing messages
def on_publish(mosq, userdata, mid):
    print("message published")
    mosq.disconnect()


### Publishing messages to S3 bucket 
def publishFile(topic, subtopic, bucketName, fileName):
    client = boto3.client('s3')
    # Open json file locally for uploading 
    data = open("messagingData/" + fileName, 'rb')
    client.put_object(
        Bucket=bucketName, 

        # File upload destination directory/fileName
        Key=topic + "/" + fileName,
        
        # File to upload
        Body= data,   
        
        # Tag file with key: value, where key is the topic name and value is the associated subtopic
        Tagging= topic + "=" + subtopic
        
    )   
    


#setConnection("thaij", "password", "35.87.51.20")
publishMessage("health", "test", "thaij", "password", "35.87.51.20")