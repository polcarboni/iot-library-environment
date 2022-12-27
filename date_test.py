import datetime
import time
from Hardware.simulator import Library

sample_time = 4
delta = datetime.timedelta(0, sample_time)
date = datetime.datetime(2022, 6, 13, 9, 30, 0)

#Stanze biblioteche
rooms=['ingresso', 'bra1', 'bra2', 'bra3']
dief_rooms =['ingresso', 'lev0', 'lev1', 'acquario']
bsi_rooms = ['ingresso', '0floor', '1floor', '100posti']

#Definizione e parametri biblioteche
Giuri = Library("Giuridica", rooms, 10, 18, 40, 200)
dief = Library("DIEF", dief_rooms, 15, 20, 60, 200, 8, 18)
BSI = Library("BSI", bsi_rooms, 0, 22, 40, 200, 10, 23)


while True: #AGGIUNGERE CONDIZIONE DI STOP (data fine registrazioni)

    #Genera dato biblioteca (passa orario)
    print(date, '\n')
    h = date.hour
    m = date.min

    Giuri.generate_values(h, m)
    dief.generate_values(h,m)


    print('\n')
    date = date + delta

    time.sleep(sample_time)




