import datetime
import time
from Hardware.simulator import Library

sample_time = 4
delta = datetime.timedelta(0, sample_time)
date = datetime.datetime(2022, 6, 13, 9, 30, 0)

#Definizione e parametri biblioteche
Giuri = Library("Giuridica", 0, max_places=200, opening=10, closing=14)
while True: #AGGIUNGERE CONDIZIONE DI STOP (data fine registrazioni)

    #Genera dato biblioteca (passa orario)
    print(date)
    h = date.hour
    m = date.min
    Giuri.generate_value(h, m)
    date = date + delta

    time.sleep(sample_time)




