from setuptools import setup

setup(
    name="mcMqttComms",
    version="0.0.4",
    description="Module for handling mission control messages to be sent to a Drone via MQTT.",
    packages= [],
    author="Jonathan Thai",
    author_email="thaijonathan53@gmail.com",      
    install_requires = ["boto3", "paho-mqtt"]
      
      
      )


