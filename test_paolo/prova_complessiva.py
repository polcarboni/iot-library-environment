from atexit import register
import paho.mqtt.client as mqtt
import threading, time, json
import random

from bridgetest import Bridge
from publishertest import Client

    
def main():
    broker_ip = "127.0.0.1"
    broker_port = 1883

    my_bridge = Bridge()
    my_bridge.setup()

    '''
    my_client = Client()
    my_client.on_connect()
    print("Connecting to " + broker_ip + " port: " + str(broker_port))
    my_client.connect(broker_ip, broker_port)
    '''

    while True:
        '''
        t1 = threading.Thread(target = my_bridge.loop())
        t2 = threading.Thread(target = my_client.loop())

        t1.start()
        t2.start()
        t1.join()
        t2.join()
        '''
        my_bridge.loop()

        if (my_bridge.inbuffer == []):
            print(my_bridge.vals)


if __name__ == "__main__":
    main()