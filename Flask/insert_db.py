from argparse import Action
from cv2 import sort

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


result = db_biblioteche.delete_many({})
