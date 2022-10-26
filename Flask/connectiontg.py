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

#---------------------------- PARTE FLASK --------------------------------

# Inizializzazione Flask
TOKEN = "5657535367:AAG9fp0SBQcdM3mreL6sTs5jxF1kDoBKv-o"
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

def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }

    r = requests.post(url, json=payload)
    return r

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()

        chat_id, txt = parse_message(msg)
        if txt == "hi":
            tel_send_message(chat_id,"hello!!")
        else:
            tel_send_message(chat_id, 'from webhook')

        return Response('ok', status= 200)
    else:
        return "<h1>Welcome!</h1>"

#Connessione a flask
myip = '127.0.0.1'
t2 = threading.Thread(target=app.run, kwargs={'host': myip})

if __name__ == '__main__':
    #t1.start()
    t2.start()
    #t1.join()
    t2.join()