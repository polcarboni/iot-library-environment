import datetime
import time
from Hardware.simulator import Library

sample_time = 4
delta = datetime.timedelta(0, sample_time)
date = datetime.datetime(2022, 6, 13, 9, 30, 0)

#Stanze biblioteche
rooms=['ingresso', 'r1', 'r2', 'r3']
dief_rooms =['ingresso', 'l0', 'l1', 'acquario']

#Definizione e parametri biblioteche
Giuri = Library("Giuridica", rooms, 10, 18, 40, 200)
dief = Library("DIEF", dief_rooms, 300, 20, 60, 300, 8, 18)


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




