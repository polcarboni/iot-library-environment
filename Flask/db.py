from argparse import Action

from matplotlib.style import available
from flask import Flask, redirect, url_for, request, jsonify, Response
from flask_cors import CORS
import paho.mqtt.client as mqtt
import threading
import pymongo
from pymongo import MongoClient
import datetime
import json

# CONNESSIONE A MONGODB
client = MongoClient("mongodb://localhost:27017")
db = client.IoT_prova
db_biblioteche = db.Biblioteche
#print(client.server_info())

# PROVA DI DIZIONARIO PER BIBLIOTECHE
dief_0 = {'name': 'bibliotecca_dief', 'room': 0,
                'h': datetime.datetime.today().hour,
                'm': datetime.datetime.today().minute,
                'day': datetime.datetime.today().day,
                'month': datetime.datetime.today().month,
                'year': datetime.datetime.today().year,
                'date': datetime.datetime.today(),
                'temperature': 'temperatura',
                'humidity': 'umidita',
                'decibel': 'decibel'}


#------------------------- PARTE MQTT ----------------------------------
#topic
registra = 'biblioteche/+/+/registra'
entrata = 'biblioteche/+/+/entrata'
uscita = 'biblioteca/+/+/uscita'

#Connessione ad MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt_client.subscribe(registra)
    mqtt_client.subscribe(entrata)
    mqtt_client.subscribe(uscita)

#Arrivo di un messaggio da parte del rasp
def on_message(client, userdata, message):
    print('message, topic -->' + message.topic +'<--' )
    biblioteca = message.topic.split('/')[1]
    stanza = message.topic.split('/')[2]

    #Inserimento nel database dei dati registrati dal rasp
    if mqtt.topic_matches_sub(registra, message.topic):
        print('nuovo messaggio su topic registra')
        message_payload = json.loads(str(message.payload.decode("utf-8")))
        registrati = {'biblioteca': biblioteca, 'stanza': stanza,
                        'temperature': message_payload['temperatura'],
                        'humidity': message_payload['umidita'],
                        'decibel': message_payload['decibel'],
                        'date': datetime.datetime.today(),
                        'place': 25,
                        'max_place': 25,
                        'available': True}
        print("I dati appena ricevuti sono:")
        print(registrati)
        db_biblioteche.insert_one(registrati)
    
    #Entrata di una persona e modifica dei posti
    if mqtt.topic_matches_sub(entrata, message.topic):
        print("Persona in entrata")
        query = {"biblioteca": {"$regex": "dief"}, "stanza": {"$regex": "piano_0"}}
        result = db_biblioteche.find_one(query, {"date": 1, "place": 1}, sort=[("_id", pymongo.DESCENDING)])
        n = result['place'] - 1
        value = {"$set": {"place": n}}
        result = db_biblioteche.update_one({'_id': result['_id']}, value)   

    #Uscita di una persona
    if mqtt.topic_matches_sub(uscita, message.topic):
        print("Persona in uscita")
        query = {"biblioteca": {"$regex": "dief"}, "stanza": {"$regex": "piano_0"}}
        result = db_biblioteche.find_one(query, {"date": 1, "place": 1}, sort=[("_id", pymongo.DESCENDING)])
        n = result['place'] + 1
        value = {"$set": {"place": n}}
        result = db_biblioteche.update_one({'_id': result['_id']}, value)


mqtt_client = mqtt.Client('my_id')
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

broker_ip = "127.0.0.1"
broker_port = 1883

print("Connecting to " + broker_ip + " port: " + str(broker_port))
mqtt_client.connect(broker_ip, broker_port)

t1 = threading.Thread(target=mqtt_client.loop_forever)

if __name__ == '__main__':
    t1.start()
    #t2.start()
    t1.join()
    #t2.join()