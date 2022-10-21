import paho.mqtt.client as mqtt
import threading, time, json

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt_client.subscribe(topic_dati)

def on_message(client, userdata, message):
    #p_id = message.topic.split('/')[2]
    #print(f"NEW MESSAGE on {message.topic} -- {p_id}")
    if mqtt.topic_matches_sub(topic_dati, message.topic):
        data = json.loads(message.payload.decode("utf-8"))
        print('ricevuto: ', data)
    
broker_ip = "127.0.0.1"
broker_port = 1883
#'/biblioteche/dief/piano_0/aula_0'
topic_dati = 'biblioteche/+/+/+'


mqtt_client = mqtt.Client('subscriber')
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


print("Connecting to " + broker_ip + " port: " + str(broker_port))
mqtt_client.connect(broker_ip, broker_port)


t1 = threading.Thread(target = mqtt_client.loop_forever)
t1.start()
t1.join()
