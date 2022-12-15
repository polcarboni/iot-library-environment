from atexit import register
import paho.mqtt.client as mqtt
import threading, time, json
import random
import time
from statistics import mean

from bridgetest import Bridge
#from publishertest import Client


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    
def register(value_dict):
    my_client.publish('biblioteche/dief/piano_0/registra', json.dumps(value_dict))
    return

def entrata():
    print("ENTRATA")
    my_client.publish('biblioteche/dief/piano_0/entrata')

def uscita():
    print("USCITA")
    my_client.publish('biblioteche/dief/piano_0/uscita')

def env_score(t, h):

    score = 0
    return score

def noise_score(n0, n1, n2, n3):
    
    tot = n0 + n1 + n2 + n3
    p0 = n0/tot
    p1 = n1/tot
    p2 = n2/tot
    p3 = n3/tot

    score = 10000

    return score
    


def main():
        
    check = 0

    noise_0 = 0
    noise_1 = 0
    noise_2 = 0
    noise_3 = 0
    
    temp = []
    hum = []
    

    while True:
    
        my_bridge.loop()
        
        if my_bridge.vals[7] != check:  #Arrivo di nuovi dati

            print(my_bridge.vals)

            if (my_bridge.vals[2] > 0):
                uscita()
                
            
            elif (my_bridge.vals[2] < 0):
                entrata()
                
            noise_0 = noise_0 + my_bridge.vals[3]
            noise_1 = noise_1 + my_bridge.vals[4]
            noise_2 = noise_2 + my_bridge.vals[5]
            noise_3 = noise_3 + my_bridge.vals[6]

            hum.append(my_bridge.vals[0])
            temp.append(my_bridge.vals[1])
        
            if my_bridge.vals[7] % 10 == 0:
                

               # datawork(temp, hum, noise_0, noise_1, noise_2, noise_3)

                
                
                t = mean(temp)
                h = mean (hum)

                env = env_score(temp, hum)
                noise = noise_score(noise_0, noise_1, noise_2, noise_3)

                media = {'temperatura': t,'umidita': h, 'overall_ambiente': env, 'decibel': noise}
                print("t: ",temp,"h: ",hum, noise_0, noise_1, noise_2, noise_3)
                print("Caccia su")
                print(media)


                temp = []
                hum = []
                noise_0 = 0 
                noise_1 = 0
                noise_2 = 0
                noise_3 = 0
                
        
        check = my_bridge.vals[7]

        
if __name__ == "__main__":


    broker_ip = "127.0.0.1"
    broker_port = 1883

    my_bridge = Bridge()
    my_bridge.setup()
    my_bridge.vals = [0, 0, 0, 0, 0, 0, 0, 0]
    
    my_client = mqtt.Client('my_id!')
    my_client.on_connect = on_connect

    print("Connecting to " + broker_ip + " port: " + str(broker_port))
    my_client.connect(broker_ip, broker_port)

    t1 = threading.Thread(target = my_client.loop_forever)
    t2 = threading.Thread(target = main)
    
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    
