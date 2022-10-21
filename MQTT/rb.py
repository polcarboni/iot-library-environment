from shutil import move
from click import command
import paho.mqtt.client as mqtt
import time, threading, json, re

parks = []


def on_connect(client, userdata, flags, rc):
    global parks
    print("Connected with result code " + str(rc))

    mqtt_client.subscribe(topic_booking)
    mqtt_client.subscribe(topic_occupied)
    mqtt_client.subscribe(topic_free)


def publish_initial_parking_info():
    init_info_topic = f'{base_topic}/{parking_id}/info'
    for x in [1, 2, 3]:
        park = {'id': 'park_' + str(x), 'state': 0}
        parks.append(park)
    mqtt_client.publish(init_info_topic, json.dumps({'position': {'nome': 'Parcheggio DIEF',
                                                                  'link': 'https://goo.gl/maps/BbKCRiopkmDHKdr18',
                                                                  'coordinates': {'lat': 44.6293165, 'lon': 10.950646}},
                                                     'data': parks, 'active': 1}), 0, True)
    print('info topic posted\n')



def on_message(client, userdata, message):
    p_id = message.topic.split('/')[2]
    #print(f"NEW MESSAGE on {message.topic} -- {p_id}")
    if mqtt.topic_matches_sub(topic_booking, message.topic):
        set_parking_lot_state(p_id, 1)
    elif mqtt.topic_matches_sub(topic_occupied, message.topic):
        set_parking_lot_state(p_id, 2)
    elif mqtt.topic_matches_sub(topic_free, message.topic):
        set_parking_lot_state(p_id, 0)

broker_ip = "127.0.0.1"
broker_port = 1883
base_topic = "parking"
parking_id = "parking_001"
message_limit = 1000
#control_topic = f'{base_topic}/{parking_id}/control'
topic_occupied = f'parking/{parking_id}/+/occupied'
topic_booking = f'parking/{parking_id}/+/booked'
topic_free = f'parking/{parking_id}/+/free'


mqtt_client = mqtt.Client(parking_id)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

print("Connecting to " + broker_ip + " port: " + str(broker_port))
mqtt_client.connect(broker_ip, broker_port)

publish_initial_parking_info()

#mqtt_client.subscribe(control_topic)

# questa funzione viene chiamata in seguito ad un segnale dell arduino che rileva con il sensore
# il movimento puo essere solo in entrata, che è equivalente a prenotare con l'app (0->1)
def parking_lot_change_state(id_p, state):
    global flag
    global flag1
    global book
    global book1
    
    for p in parks:
        if p['id'] == id_p:
            p['state'] = state
            mqtt_client.publish(f'parking/{parking_id}/{id_p}/state', state)
            print(f'\nparking state changed by sensor --> {id_p} -> {state}\n')
            if id_p == 'park_1':
                flag = True
                book = state
            if id_p == 'park_2':
                flag = True
                book1 = state
            return 0
    print("ERROR: id del parcheggio non valido")


def simulazione():
    input('\n------\n')
    #simulazione occupazione senza prenotazione
    parking_lot_change_state('park_2', 1)
    input('\n------\n')

# lo stato del parcheggio cambia perche è stato prenotato/confermato dal SAP
# devo comunicare all arduino di cambiare stato
def set_parking_lot_state(id_p, state):
    global flag
    global book
    global book1
    #print(f'changing {id_p} to {state} ... \n')
    if id_p == 'park_1':
        for p in parks:
            if p['id'] == id_p:
                p['state'] = state
                print(f'\nparking state changed by app --> {id_p} -> {state}\n')
                
                if state == 3:
                    print('\nallarme\n')
                
                flag = True
                book = state
    if id_p == 'park_2':
        for p in parks:
            if p['id'] == id_p:
                p['state'] = state
                print(f'parking state changed by app --> {id_p} -> {state}')
                
                if state == 3:
                    print('\nallarme\n')
                
                flag = True
                book1 = state
flag = False
flag1 = False
flag2 = 0
book = -1
book1 = -1
movreale = -1
movsimulato = -1
line = -1

import serial
def serial_communication():
    global flag
    global flag1
    global flag2
    global book
    global book1
    global movreale
    global movsimulato
    global line
    
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser1 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)

    inbuffer = []
    inbuffer1 = []

    while True:

        if not ser is None:

            if ser.in_waiting > 0:
                # data available from the serial port
                lastchar = ser.read(1)

                if lastchar == b'\xfe':  # EOL
                    #print("\nValue received")
                    # I have received a line from the serial port. I can use it
                    if len(inbuffer) < 3:  # at least header, size, footer
                        return False
                    # split parts
                    if inbuffer[0] != b'\xff':
                        return False

                    mov = int.from_bytes(inbuffer[3], byteorder='little')
                    strmov = "Sensor value: %d " % (mov)
                    #print(strmov)

                    movreale = int.from_bytes(inbuffer[3], byteorder='little')
                    if movreale==0:
                        movreale=-1
                    strmovreale = "Sensor movreale: %d " % (movreale)
                    #print(strmovreale)
                    

                    alarm = int.from_bytes(inbuffer[4], byteorder='little')
                    stralarm = "Alarm value: %d " % (alarm)
                    #print(stralarm)
                    if alarm==1:
                        topic_allarme = f'parking/{parking_id}/park_1/allarme'
                        mqtt_client.publish(topic_allarme, '1')

                    if mov==1 and book==-1 and line==0:
                        #print("\nil sensore ha rilevato un movimento\n")
                        parking_lot_change_state('park_1', 1)
                    if mov==0 and book==0:
                        #print("\nil sensore ha rilevato un movimento\n")
                        book = -1
                        flag = True
                    inbuffer = []
                    if book == -1:
                        flag1 = True
                else:
                    # append
                    inbuffer.append(lastchar)

        if not ser1 is None:

            if ser1.in_waiting > 0:
                # data available from the serial port
                lastchar1 = ser1.read(1)

                if lastchar1 == b'\xfe':  # EOL
                    #print("\nValue received from serial simulata")
                    if len(inbuffer1) < 3:  # at least header, size, footer
                        return False
                    # split parts
                    if inbuffer1[0] != b'\xff':
                        return False
                    movsimulato = int.from_bytes(inbuffer1[3], byteorder='little')
                    strmovsimulato = "Sensor movsimulato: %d " % (movsimulato)
                    #print(strmovsimulato)
                    line = int.from_bytes(inbuffer1[4], byteorder='little')
                    strline = "Sensor line: %d " % (line)
                    #print(strline)

                    alarm1 = int.from_bytes(inbuffer1[5], byteorder='little')
                    stralarm1 = "Alarm value: %d " % (alarm1)
                    #print(stralarm1)
                    if alarm1==1:
                        topic_allarme = f'parking/{parking_id}/park_2/allarme'
                        mqtt_client.publish(topic_allarme, '1')

                    if movsimulato==1 and book1==-1 and line==0:
                        #print("\nil sensore ha rilevato un movimento\n")
                        parking_lot_change_state('park_2', 1)
                    if movsimulato==0 and book1==0:
                        #print("\nil sensore ha rilevato un movimento\n")
                        book1 = -1
                        flag = True
                    inbuffer1 = []
                    if book1 == -1:
                        flag1 = True
                else:
                    # append
                    inbuffer1.append(lastchar1)

        if movreale == 1 and line == 1 and movsimulato == 0 and flag2 == 0:
            parking_lot_change_state('park_1', 2)
            parking_lot_change_state('park_2', 2)
            flag2 = 1

        if movsimulato == 1 and line == 1 and movreale == -1 and flag2 == 0:
            parking_lot_change_state('park_1', 2)
            parking_lot_change_state('park_2', 2)
            flag2 = 1
        
        if movreale == -1 and line == 0 and movsimulato == 0 and flag2 == 1:
            parking_lot_change_state('park_1', 0)
            parking_lot_change_state('park_2', 0)
            book = -1
            book1 = -1
            flag2 = 0


        if flag:
            #print('sending state normal')
            if book == 0 or book == -1 and line==0:
                ser.write(b'0')
                #print(0)
            if book == 1 and line==0:
                ser.write(b'1')
                #print(1)
            if book == 2 and line==0:
                ser.write(b'2')
                #print(2)
            if book1 == 0 or book1 == -1 and line==0:
                ser1.write(b'0')
                #print(0)
            if book1 == 1 and line==0:
                ser1.write(b'1')
                #print(1)
            if book1 == 2 and line==0:
                ser1.write(b'2')
                #print(2)
            
            flag=False

        if flag1:        
            #print('sending state anomalo')
            #reale ha parcheggiato male: accendo il suo led e quello di simulato (reale paga doppio)
            if movreale == 1 and line == 1 and movsimulato == 0:
                #print('park1: tariffa doppia')
                ser.write(b'4')
                #print(4)
                ser1.write(b'5')
                #print(4)
                #parking_lot_change_state('park_1', 2)
                #parking_lot_change_state('park_2', 2)

            #simulato ha parcheggiato male: accendo il suo led e quello di reale (simulato paga doppio)
            if movsimulato == 1 and line == 1 and movreale == -1:
                #print('park2: tariffa doppia')
                ser.write(b'5')
                #print(5)
                ser1.write(b'4')
                #print(5)
                #parking_lot_change_state('park_1', 2)
                #parking_lot_change_state('park_2', 2)

            #liberazione in entrambi i casi: spengo entrambi i led
            if movreale == -1 and line == 0 and movsimulato == 0:
                if book != 1 and book1 != 1:
                    ser.write(b'3')
                    #print(3)
                    ser1.write(b'3')
                    #print(3)
                    #if book==2:
                        #parking_lot_change_state('park_1', 0)
                        #parking_lot_change_state('park_2', 0)
                else:
                    pass
            
            flag1 = False
    
t1 = threading.Thread(target=simulazione)
t2 = threading.Thread(target=mqtt_client.loop_forever)
t3 = threading.Thread(target=serial_communication)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
    

