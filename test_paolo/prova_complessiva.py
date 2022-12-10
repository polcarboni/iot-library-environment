from atexit import register
import paho.mqtt.client as mqtt
import threading, time, json
import random
import time

from bridgetest import Bridge
from publishertest import Client

'''
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    
def register(media):
    my_client.publish('biblioteche/dief/piano_0/registra', json.dumps(media))
    return

def entrata():
    my_client.publish('biblioteche/dief/piano_0/entrata')

def uscita():
    my_client.publish('biblioteche/dief/piano_0/uscita')

def dataWork(values):
    pass
'''

    
def main():
    check = 0

    noise_0 = 0
    noise_1 = 0
    noise_2 = 0
    noise_3 = 0
    
    temp = []
    hum = []

    broker_ip = "127.0.0.1"
    broker_port = 1883

    my_bridge = Bridge()
    my_bridge.setup()
    my_bridge.vals = [0, 0, 0, 0, 0, 0, 0, 0]

    '''
    my_client = Client()
    my_client.on_connect()
    print("Connecting to " + broker_ip + " port: " + str(broker_port))
    my_client.connect(broker_ip, broker_port)
    '''

    while True:
    
        my_bridge.loop()
        
        if my_bridge.vals[7] != check:  #Arrivo di nuovi dati

            print(my_bridge.vals)

            if (my_bridge.vals[2] > 0):
                #uscita()
                print("USCITA")
                pass
            
            elif (my_bridge.vals[2] < 0):
                #entrata()
                print("ENTRATA")
                pass
            
            noise_0 = noise_0 + my_bridge.vals[3]
            noise_1 = noise_1 + my_bridge.vals[4]
            noise_2 = noise_2 + my_bridge.vals[5]
            noise_3 = noise_3 + my_bridge.vals[6]

            hum.append(my_bridge.vals[0])
            temp.append(my_bridge.vals[1])
        
            if my_bridge.vals[7] % 10 == 0:
                print("Caccia su")
                print("t: ",temp,"h: ",hum, noise_0, noise_1, noise_2, noise_3)
                temp = []
                hum = []
                noise_0 = 0 
                noise_1 = 0
                noise_2 = 0
                noise_3 = 0
                
        
        check = my_bridge.vals[7]

        
if __name__ == "__main__":
    main()