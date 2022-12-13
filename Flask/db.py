from argparse import Action
from ast import parse

from matplotlib.style import available
from flask import Flask, redirect, url_for, request, jsonify, Response
from flask_cors import CORS
import requests
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
        registrati = {'biblioteca': "giuridica", 'stanza': stanza,
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

#---------------------------- PARTE FLASK --------------------------------

# Inizializzazione Flask
TOKEN = "5657535367:AAG9fp0SBQcdM3mreL6sTs5jxF1kDoBKv-o" #Inserire qui bot di telegram
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#Lettura del messaggio
def parse_message(message):
    print("message-->", message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print('chat_id-->', chat_id)
    print('txt-->', txt)
    return chat_id, txt
 
# Lista iniziale di telegram che mostra le biblioteche presenti nel database
def lista_biblioteche(chat_id, biblioteche):
    output = ""
    for bib in biblioteche:
        output+= "\n/"+ bib
    print(biblioteche)
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': "Digita la biblioteca che vuoi visualizzare:\n"+output[1:]
    }

    r = requests.post(url, json=payload)
    return r

# Lista per capire cosa si vuole vedere
def opzioni(chat_id, biblioteca):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': "Selezionare l'azione che si vuole compiere:\n"
            "/Info_"+biblioteca+"\n"
            "/Posizione_"+biblioteca+"\n"
            "/FasciaOraria_"+biblioteca
    }

    r = requests.post(url, json=payload)
    return r

# Funzione per restituire le info di una biblioteca all'ora in cui si cerca
def info(chat_id, biblioteca):
    query = {"biblioteca": {"$regex": biblioteca}, "stanza": {"$regex": "piano_0"}}
    result = db_biblioteche.find_one(query, {"_id":0, "temperature": 1, "humidity": 1, "decibel": 1, "place": 1, "avaible": 1}, sort=[("_id", pymongo.DESCENDING)])
    print(result)
    output = ""
    for key, value in result.items():
        output+= "\n"+ str(key) + ": " + str(value)

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': output
    }

    r = requests.post(url, json=payload)
    return r 

@app.route('/', methods = ['GET', 'POST'])
def index():
    biblioteche = db_biblioteche.distinct("biblioteca")
    if request.method == 'POST':
        msg = request.get_json()

        chat_id, txt = parse_message(msg)
        if txt == "/start":
            lista_biblioteche(chat_id, biblioteche)
        elif txt[1:] in biblioteche:
            r = opzioni(chat_id, txt[1:])
        elif txt[:5] == "/Info":
            info(chat_id, txt[6:])

        return Response('ok', status= 200)

#Connessione a flask
myip = '127.0.0.1'
t2 = threading.Thread(target=app.run, kwargs={'host': myip})

if __name__ == '__main__':
    t1.start()
    t2.start()
    t1.join()
    t2.join()