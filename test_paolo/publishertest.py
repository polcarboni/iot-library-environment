import serial
import serial.tools.list_ports
import paho.mqtt.client as mqtt
import threading

from bridgetest import Bridge

def on_connect(client, userdata,flags, rc):
    print("Connesso con result code: " + str(rc))
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    pass
    #print(msg.topic + " " + str(msg.payload))


def main():
    #broker_ip = "127.0.0.1"
    #broker_port = 1883

    my_bridge = Bridge()
    my_bridge.setup()


    my_client = mqtt.Client("Clientes")
    my_client.on_connect = on_connect
    my_client.on_message = on_message

    my_client.connect("mqtt.eclipseprojects.io", 1883, 60)



if __name__ == "__main__":
    main()

