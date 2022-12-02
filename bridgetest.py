import serial
import serial.tools.list_ports
import paho.mqtt.client as mqtt

class Bridge():

    def setupSerial(self):

        self.encoding = 'utf-8'
        self.ser = None
        self.portname = None
        self.inbuffer = []
        
        print("Porte disponibili: ")

        ports = serial.tools.list_ports.comports()
        
        for port in ports:
            print (port.device)
            print (port.description)
            
            self.portname = port.device
        
        try:
            if self.portname is not None:
                self.ser = serial.Serial(self.portname, 9600, timeout = 0)
        except:
            self.ser = None        

    def setupMQTT(self):
        pass

    def on_connect(self):
        pass

    def on_message(self, client, userdata, msg):
        pass

    def loop(self):
        while(True):
            str = ""
            if not self.ser is None:
                if self.ser.in_waiting > 0:
                    lastchar = self.ser.read(1)
                
                    

                    if lastchar == b'x':
                        print(str.join(self.inbuffer))
                        self.inbuffer = []
                    
                    else:
                        dec = lastchar.decode(self.encoding)
                        self.inbuffer.append(dec)
                        
                    
                        
def main():
    bridge = Bridge()
    bridge.setupSerial()
    bridge.loop()

if __name__ == "__main__":
    main()