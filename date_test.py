import datetime
import time
import sys, os

from Hardware.library_gen import Library

sample_time = 4
delta = datetime.timedelta(0, sample_time)
date = datetime.datetime(2022, 6, 13, 9, 59, 50)

#Stanze biblioteche
giuri_rooms = ['ingresso', 'east', 'west', 'north', 'south']
dief_rooms =['ingresso', 'lev0', 'lev1', 'acquario']
bsi_rooms = ['ingresso', '0floor', '1floor', '100posti']

#Definizione e parametri biblioteche
#Nome, stanze, temp media, hum media, posti max, apertura, chiusura
Giuri = Library("Giuridica", giuri_rooms, 18, 40, 200, 8, 0, 20, 0)
dief = Library("DIEF", dief_rooms, 20, 60, 200, 9, 0, 19, 30)
BSI = Library("BSI", bsi_rooms, 6, 20, 200, 10, 0, 23, 0)
#ax = Library("name", giuri_rooms, 17.2, 64.3, 200, 9, 22)

i = 0
while True: 

    #Genera dato biblioteca (passa orario)
    print('\n', date, '\n')
    h = date.hour
    m = date.minute


    Giuri.generate_values(h, m)
    dief.generate_values(h,m)
    BSI.generate_values(h,m)

    sys.stdout=open(os.devnull, 'w')

    date = date + delta
    i = i + 1 

    if i%200 == 0:
        sys.stdout = sys.__stdout__
        
#    time.sleep(2)




