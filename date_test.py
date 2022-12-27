import datetime
import time
from Hardware.simulator import Library

sample_time = 4
delta = datetime.timedelta(0, sample_time)
date = datetime.datetime(2022, 6, 13, 6, 59, 0)

#Stanze biblioteche
giuri_rooms = ['ingresso', 'east', 'west', 'north', 'south']
dief_rooms =['ingresso', 'lev0', 'lev1', 'acquario']
bsi_rooms = ['ingresso', '0floor', '1floor', '100posti']

#Definizione e parametri biblioteche
#Nome, stanza, posti occupati, temp media, hum media, posti max, apertura, chiusura
Giuri = Library("Giuridica", giuri_rooms, 18, 40, 200, 8, 20)
dief = Library("DIEF", dief_rooms, 20, 60, 200, 9, 22)
BSI = Library("BSI", bsi_rooms, 22, 40, 200, 10, 23)
ax = Library("name", giuri_rooms, 17.2, 64.3, 200, 9, 22)


while True: #AGGIUNGERE CONDIZIONE DI STOP (data fine registrazioni)

    #Genera dato biblioteca (passa orario)
    print(date, '\n')
    h = date.hour
    m = date.min

    Giuri.generate_values(h, m)
    dief.generate_values(h,m)
    BSI.generate_values(h,m)


    print('\n')
    date = date + delta

    #time.sleep(3)




