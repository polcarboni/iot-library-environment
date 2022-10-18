from flask import Flask, redirect, url_for, request, jsonify, Response
from flask_cors import CORS
import paho.mqtt.client as mqtt
import threading

#roba MQTT
topic_1 = 'topic/a/cui/mi/voglio/iscrivere'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    mqtt_client.subscribe(topic_1)


def on_message(client, userdata, message):
    print('message, topic -->' + message.topic +'<--' )
    message_payload = json.loads(str(message.payload.decode("utf-8")))
    print(f'message payload: \n{message_payload}')
    if mqtt.topic_matches_sub(topic_1, message.topic):
        print('nuovo messaggio su topic 1')


mqtt_client = mqtt.Client('my_id')
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

broker_ip = "127.0.0.1"
broker_port = 9879

print("Connecting to " + broker_ip + " port: " + str(broker_port))
mqtt_client.connect(broker_ip, broker_port)

t1 = threading.Thread(target=mqtt_client.loop_forever)


#roba Flask
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/example', methods=['GET'])
def example():
    return {'sucess': True}
# http://127.0.0.1:5000/example

myip = '127.0.0.1'
t2 = threading.Thread(target=app.run, kwargs={'host': myip})


if __name__ == '__main__':
    t1.start()
    t2.start()
    t1.join()
    t2.join()