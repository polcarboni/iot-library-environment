import datetime
import time
import sys, os

from Hardware.library_gen import Library

sample_time = 1800
delta = datetime.timedelta(0, sample_time)
date = datetime.datetime(2023, 1, 3, 6, 59, 50)

#Stanze biblioteche
#giuri_rooms = ['ingresso', 'east', 'west', 'north', 'south']
#dief_rooms =['ingresso', 'lev0', 'lev1', 'acquario']
#bsi_rooms = ['ingresso', '0floor', '1floor', '100posti']
giuri_rooms = ['ingresso']
dief_rooms =['ingresso']
bsi_rooms = ['ingresso']

#Definizione e parametri biblioteche
#Nome, stanze, temp media, hum media, posti max, apertura, chiusura
Giuri = Library("Giuridica", giuri_rooms, 18, 40, 44.643841611688345, 10.925390361381135, 200, 8, 0, 20, 0)
dief = Library("DIEF", dief_rooms, 20, 60, 44.62996350275527, 10.9487978, 200, 9, 0, 19, 30)
BSI = Library("BSI", bsi_rooms, 6, 20, 44.63116602207506, 10.943921424257166, 200, 10, 0, 23, 0)
#ax = Library("name", giuri_rooms, 17.2, 64.3, 200, 9, 22)

i = 0
while date < datetime.datetime.today(): 

    #Genera dato biblioteca (passa orario)
    h = date.hour
    m = date.minute
    weekday = date.weekday()
    print('\n', date, ' ', weekday, '\n')


    Giuri.generate_values(h, m, date)
    dief.generate_values(h,m, date)
    BSI.generate_values(h,m, date)

    #sys.stdout=open(os.devnull, 'w')

    date = date + delta
    i = i + 1 

    #if i%200 == 0:
    #    sys.stdout = sys.__stdout__
        
#    time.sleep(2)




