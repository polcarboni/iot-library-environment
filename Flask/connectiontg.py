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
    query = {"biblioteca": {"$regex": biblioteca}, "stanza": {"$regex": "ingresso"}}
    result = db_biblioteche.find_one(query, {"_id":0, "temperature": 1, "humidity": 1, "decibel": 1, "place": 1}, sort=[("_id", pymongo.DESCENDING)])
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

# Funzione per trovare la biblioteca migliore
def portami(chat_id):
    biblioteche = []
    out = ""
    for testy in db_biblioteche.find().distinct('biblioteca'):
        biblioteche.append(testy)

    best = {"biblioteca": None, "overal_ambiente": -3, "decibel": 0, "place": None}
    for testy in biblioteche:
        query = {"biblioteca": {"$regex": testy}, "stanza": {"$regex": "ingresso"}}
        result = db_biblioteche.find_one(query, {"_id":0, "biblioteca": 1, "overal_ambiente": 1, "decibel": 1, "place": 1}, sort=[("_id", pymongo.DESCENDING)])
        print(result)
        abs_amb_re = abs(result['overal_ambiente'])
        abs_amb_be = abs(best['overal_ambiente'])
        if abs_amb_re < abs_amb_be and result['decibel'] > best['decibel'] and result["place"]:
            for key, value in result.items():
                best[key] = result[key]
        
    out = out + "*Biblioteca: " + best["biblioteca"] + "*\n\n"
    out = out + "Temperatura: "

    if best["overal_ambiente"] == -2:
        out = out + "Freddissima \U0001F976 \n"
    elif best["overal_ambiente"] == -1:
        out = out + "Fredda \U0001F914 \n"
    elif best["overal_ambiente"] == 0:
        out = out + "Perfetta \U0001F917 \n"
    elif best["overal_ambiente"] == 1:
        out = out + "Calda \U0001F914 \n"
    elif best["overal_ambiente"] == 2:
        out = out + "Caldissima \U0001F975 \n"

    out = out + "Rumore: "
    if best["decibel"] >=0 and best["decibel"] <= 3:
        out = out + "Rumorosissima \U0001FAE3 \n"
    elif best["decibel"] >=4 and best["decibel"] <= 5:
        out = out + "Rumorosa \U0001FAE2 \n"
    elif best["decibel"] >=6 and best["decibel"] <= 8:
        out = out + "Silenziosa \U0001F92B \n"
    elif best["decibel"] >=9 and best["decibel"] <= 10:
        out = out + "Perfetta \U0001FAE1 \n"

    out = out + "Posti disponibili: " + str(best["place"]) + "\n"

    

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': out,
                'parse_mode': 'Markdown'
            }
   
    r = requests.post(url,json=payload)
    return r, best["biblioteca"]

#Funzione per vedere la mappa
def mappa(chat_id, biblioteca):
    
    query = {"biblioteca": {"$regex": biblioteca}, "stanza": {"$regex": "ingresso"}}
    result = db_biblioteche.find_one(query, {"_id":0, "lat": 1, "long": 1}, sort=[("_id", pymongo.DESCENDING)])

    url = f'https://api.telegram.org/bot{TOKEN}/sendLocation'
    payload = {
                'chat_id': chat_id,
                'longitude': result['lat'],
                'latitude': result['long']
            }

    r = requests.post(url,json=payload)
    return r

#Stampa giorni della settimana
def giorni(chat_id):

    out = "/lunedi\n/martedi\n/mercoledi\n/giovedi\n/venerdi\n/sabato"

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': out
            }

    r = requests.post(url, json=payload)
    return r

#Predizione della settimana
def predizione(chat_id, weekday):
    biblioteche = []
    out = ""
    for testy in db_biblioteche.find().distinct('biblioteca'):
        biblioteche.append(testy)

    best = {"biblioteca": None, "overal_ambiente": -3, "decibel": 0, "weekday": None}
    for testy in biblioteche:
        query = {"biblioteca": {"$regex": testy}, "stanza": {"$regex": "ingresso"}, "weekday": weekday}
        result = db_biblioteche.find_one(query, {"_id":0, "biblioteca": 1, "overal_ambiente": 1, "decibel": 1, "weekday": 1}, sort=[("_id", pymongo.DESCENDING)])
        print(result)
        abs_amb_re = abs(result['overal_ambiente'])
        abs_amb_be = abs(best['overal_ambiente'])
        if abs_amb_re < abs_amb_be and result['decibel'] > best['decibel']:
            for key, value in result.items():
                best[key] = result[key]
        
    out = out + "*Biblioteca: " + best["biblioteca"] + "*\n\n"
    out = out + "Temperatura: "

    if best["overal_ambiente"] == -2:
        out = out + "Freddissima \U0001F976 \n"
    elif best["overal_ambiente"] == -1:
        out = out + "Fredda \U0001F914 \n"
    elif best["overal_ambiente"] == 0:
        out = out + "Perfetta \U0001F917 \n"
    elif best["overal_ambiente"] == 1:
        out = out + "Calda \U0001F914 \n"
    elif best["overal_ambiente"] == 2:
        out = out + "Caldissima \U0001F975 \n"

    out = out + "Rumore: "
    if best["decibel"] >=0 and best["decibel"] <= 3:
        out = out + "Rumorosissima \U0001FAE3 \n"
    elif best["decibel"] >=4 and best["decibel"] <= 5:
        out = out + "Rumorosa \U0001FAE2 \n"
    elif best["decibel"] >=6 and best["decibel"] <= 8:
        out = out + "Silenziosa \U0001F92B \n"
    elif best["decibel"] >=9 and best["decibel"] <= 10:
        out = out + "Perfetta \U0001FAE1 \n"

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': out,
                'parse_mode': 'Markdown'
            }
   
    r = requests.post(url,json=payload)
    return r

@app.route('/', methods = ['GET', 'POST'])
def index():
    biblioteche = db_biblioteche.distinct("biblioteca")
    weekday = ["/lunedi", "/martedi", "/mercoledi", "/giovedi", "/venerdi", "/sabato"]
    if request.method == 'POST':
        msg = request.get_json()

        chat_id, txt = parse_message(msg)
        if txt == "/start":
            lista_biblioteche(chat_id, biblioteche)
        elif txt[1:] in biblioteche:
            r = opzioni(chat_id, txt[1:])
        elif txt[:5] == "/Info":
            info(chat_id, txt[6:])
        elif txt[:10] == "/Posizione":
            mappa(chat_id, txt[11:])
        elif txt == "/portami":
            r, biblioteca = portami(chat_id)
            mappa(chat_id, biblioteca)
        elif txt == "/giorni":
            giorni(chat_id)
        elif txt in weekday:
            predizione(chat_id, weekday.index(txt))
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