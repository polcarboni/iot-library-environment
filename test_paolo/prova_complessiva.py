from atexit import register
import paho.mqtt.client as mqtt
import threading, time, json
import random

from bridgetest import Bridge
from publishertest import 

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def register():
    pass

    
def main():
    my_bridge = Bridge()
    my_bridge.setup()

    ix = 0

    while True:
        t1 = threading.Thread(target = my_bridge.loop())
        t2 = threading.Thread(target = )

        t1.start()
        t2.start()
        t1.join()
        t2.join()



if __name__ == "__main__":
    main()