from setuptools import setup, find_packages

setup(
    name="mcMqttComms",
    version="0.0.8",
    description="Module for handling mission control messages to be sent to a Drone via MQTT.",
    packages= find_packages(where="src"),
    package_dir={
    '': 'src',
    },
    author="Jonathan Thai",
    author_email="thaijonathan53@gmail.com",      
    install_requires = ["boto3", "paho-mqtt"]
      
      
      )


