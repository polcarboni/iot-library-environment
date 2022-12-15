from atexit import register
import paho.mqtt.client as mqtt
import threading, time, json
import random

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    

def register(media):
    mqtt_client.publish('biblioteche/dief/piano_0/registra', json.dumps(media))
    return

def entrata():
    print("ENTRATA")
    mqtt_client.publish('biblioteche/dief/piano_0/entrata')

def uscita():
    print("USCITA")
    mqtt_client.publish('biblioteche/dief/piano_0/uscita')

def read_data(media, n):

    t = random.randint(10, 30)
    h = random.randint(10, 30)
    d = random.randint(0, 100)


    dati = {'t': t,'h': h,'d': d}
    print(dati)
    n += 1

    media['temperatura'] = (media['temperatura']+dati['t'])/n
    media['umidita'] = (media['umidita']+dati['h'])/n
    media['decibel'] = (media['decibel']+dati['d'])/n
    media['overall_ambiente'] = random.randint(0, 3)

    return media, n


def main():
    media = {'temperatura': 0,'umidita': 0,'overall_ambiente': 0,'decibel': 0}
    n = 0
    i = 0
    disponibili = 0
    while True:
        media, n = read_data(media, n)

        # Simulazione ingressi/uscite.
        p = random.randint(0, 100)
        if i==5:
            register(media)
            i = 0
        i += 1
        if p>50:
            if p > 75:
                print("persona in entrata")
                entrata()
                disponibili = disponibili + 1
            else:
                print("Persona in uscita")
                uscita()
                disponibili = disponibili - 1
        time.sleep(3)

if __name__ == "__main__":
    broker_ip = "127.0.0.1"
    broker_port = 1883


    mqtt_client = mqtt.Client('my_id!')
    mqtt_client.on_connect = on_connect


    print("Connecting to " + broker_ip + " port: " + str(broker_port))
    mqtt_client.connect(broker_ip, broker_port)

    t1 = threading.Thread(target = mqtt_client.loop_forever)
    t2 = threading.Thread(target = main)

    t1.start()
    t2.start()

    t1.join()
    t2.join()