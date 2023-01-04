import serial
import serial.tools.list_ports

import paho.mqtt.client as mqtt


class Bridge():
    
    def setupSerial(self):
        self.ser = None
        print("Porte disponibili: ")

        ports = serial.tools.list_ports.comports()
        self.portname = None
        for port in ports:
            print (port.device)
            print (port.description)
            print(type(self.portname))

            if 'arduino' in port.description.lower():
                self.portname = port.device
                
        print ("Connessione a: " + self.portname)

        try:
            if self.portname is not None:
                self.ser = serial.Serial(self.portname, 9600, timeout = 0)
        except:
            self.ser = None

        #Buffer interno per i dati provenienti da seriale
        self.inbuffer = []
    
    def setupMQTT(self):
        self.clientMQTT = mqtt.Client()
        self.clientMQTT.on_connect = self.on_connect 
        self.clientMQTT.on_message = self.on_message 

        print("Connessione ...")

        self.clientMQTT.connect = ("127.0.0.1", 1883, 60)
        self.clientMQTT.loop_start()
    
    def on_connect(self, client, userdata, flags, rc):
        print("Connesso con result code: " + str(rc))

        #L'iscrizione a on_connect() permette la riconnessione nel caso 
        # di perdita di connessione, rieffettuando l'iscrizione.
        self.clientMQTT.subscribe("light")

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        if msg.topic == 'light':
            self.ser.write_(msg.payload)
    
    def setup(self):
        self.setupSerial()
        self.setupMQTT()

    def loop(self): #Loop infinito per la gestione della seriale
        while (True):
            if not self.ser is None:

                if self.ser.in_waiting > 0:
                # Dati disponibili dalla porta seriale

                    lastchar = self.ser.read(1)

                    if lastchar == b'\xfe': #EOL
                        print("\nRicevuto")
                        self.useData()
                        self.inBuffer = []
                    else:
                        self.inbuffer.append_(lastchar)

    def useData(self):  #Operazioni da eseguire quando si ricevono dati
        
        if len(self.inbuffer)<3:
            return False

        if self.inbuffer[0] != b'\xff':
            return False
        
        numval = int.from_bytes(self.inbuffer[1], byteorder = 'little')

        for i in range(numval):
            val = int.from_bytes(self.inbuffer[i+2], byteorder = 'little')

            strval = "Sensor %d:  %d" %(i, val)
            print(strval)
            self.clientMQTT.publish('sensor/{:d}'.format(i), '{:d}'.format(val))

def main():
    bridge = Bridge()
    bridge.setup()

if __name__ == "__main__":
    main()