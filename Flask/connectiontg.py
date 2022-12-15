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

#---------------------------- PARTE FLASK --------------------------------

# Inizializzazione Flask
TOKEN = "5657535367:AAG9fp0SBQcdM3mreL6sTs5jxF1kDoBKv-o" #Inserire qui bot di telegram
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Prove del tutorial
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
    emoji = ["\U0001F534", "\U0001F534", "\U0001F7E1", "\U0001F7E1"] #Temp, Hum, Dec, Place
    i = 0
    for key, value in result.items():
        output+= "\n"+ str(key) + ": " + str(value) + emoji[i]
        i = i + 1

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': output
    }
    r = requests.post(url, json=payload)
    return r 

#Messaggio di default in caso di errore di invio
def tel_send_message(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': "Digitare /start per iniziare"
            }
   
    r = requests.post(url,json=payload)
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
        else:
            tel_send_message(chat_id)

        return Response('ok', status= 200)

#Connessione a flask
myip = '127.0.0.1'
t2 = threading.Thread(target=app.run, kwargs={'host': myip})

if __name__ == '__main__':
    #t1.start()
    t2.start()
    #t1.join()
    t2.join()