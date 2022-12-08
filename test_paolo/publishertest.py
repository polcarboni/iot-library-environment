from atexit import register
import paho.mqtt.client as mqtt
import threading, time, json

from bridgetest import Bridge

class Client():

    def on_connect(client, userdata,flags, rc):
        print("Connesso con result code: " + str(rc))

    def register(client):
        client.publish("biblioteche/dief/piano_0/registra")

    def entrata(client):
        client.publish("biblioteche/dief/piano_0/entrata")

    def uscita(client):
        client.publish("biblioteche/dief/piano_0/uscita")

    def loop():
        pass
    


def main():
    #broker_ip = "127.0.0.1"
    #broker_port = 1883

    my_bridge = Bridge()
    my_bridge.setup()


    my_client = mqtt.Client("Clientes")
    my_client.on_connect = on_connect
    my_client.on_message = on_message

    my_client.connect("mqtt.eclipseprojects.io", 1883, 60)



